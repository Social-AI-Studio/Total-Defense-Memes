const db = require("../models");

const Meme = db.Meme;
const Batch = db.Batch;
const Screening = db.Screening;
const Pillar = db.Pillar;
const Tag = db.Tag;
const Op = db.Sequelize.Op;
const User = db.User;

const create = async (req, res) => {

  // Fetch the memes within the indicated batch
  var userPromise = User.findByPk(req.userId)
  
  var batchPromise = Batch.findOne({
    where: {
      name: req.body.batchName
    },
    include: [{
      model: Meme, as: "memes"
    }]
  })
  
  Promise.all([userPromise, batchPromise]).then(async (results) => {
    var user = results[0]
    var batch = results[1]

    // Create screenings
    var screenings = []
    batch.memes.forEach(element => {
      screenings.push({
        annotatorId: req.body.annotatorId,
        memeId: element.id
      })
    });

    await Screening.bulkCreate(screenings)

    // add batch to user
    user.addBatch(batch)

    res.status(200).send({
      message: "OK",
    });
  })
};

const update = async (req, res) => {

  // Fetch the memes within the indicated batch
  const screeningPromise = Screening.findOne({
    where: {
      id: req.params.screeningId,
    }, include: [
      { model: Pillar }
    ]
  })

  const tagPromise = Tag.findAll({
    where: {
      id: {
        [Op.in]: req.body.topicTags
      }
    }
  })

  const pillarPromise = Pillar.findAll({
    where: {
      id: {
        [Op.in]: req.body.pillars
      }
    }
  })

  Promise.all([screeningPromise, tagPromise, pillarPromise]).then(async function (results) {
    let screening = results[0];
    let tags = results[1];
    let pillars = results[2];

    // Update screening
    screening.contentType = req.body.contentType;
    screening.relatedCountry = req.body.relatedCountry;
    screening.flagged = req.body.flagged;
    screening.setTags(tags)

    screening.removePillars(screening.Pillars)
    for (let i = 0; i < pillars.length; i++) {
      const element = pillars[i];
      screening.addPillar(element, { through: { stance: req.body.stance[i] } })
    }

    await screening.save()

    res.status(200).send({
      message: "OK",
    });
  }).catch((err) => {
    res.status(500).send({
      message: err
    })
  })
};

const fetch = async (req, res) => {

  // Fetch the memes within the indicated batch
  Screening.findAll({
    where: {
      annotatorId: req.userId
    },
    include: [{
      model: Meme, 
      where: {batchId: req.params.batchId},
      required: true,
      as: "memes"
    }]
  }).then((screening) => {
    res.status(200).send({
      data: screening,
    });
  })
};

const fetchAll = async (req, res) => {

  // Fetch the memes within the indicated batch
  User.findByPk(req.userId, {
    include: [{
      model: Batch, as: "batches"
    }]
  }).then((screening) => {
    console.log(screening)
    res.status(200).send({
      data: screening.batches,
    });
  })
};

module.exports = {
  create,
  update,
  fetch,
  fetchAll
};