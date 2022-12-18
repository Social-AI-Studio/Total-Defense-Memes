const db = require("../models");

const Meme = db.Meme;
const Batch = db.Batch;
const Screening = db.Screening;
const Pillar = db.Pillar;
const Tag = db.Tag;
const Op = db.Sequelize.Op;

const create = async (req, res) => {

  // Fetch the memes within the indicated batch
  Batch.findOne({
    where: {
      name: req.body.batchName
    },
    include: [{
      model: Meme, as: "memes"
    }]
  }).then((batch) => {
    console.log(batch.memes.length)

    // Create screenings
    var screenings = []
    batch.memes.forEach(element => {
      screenings.push({
        annotatorId: req.body.annotatorId,
        memeId: element.id
      })
    });

    return Screening.bulkCreate(screenings)
  }).then((_) => {
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

  Promise.all([screeningPromise, tagPromise, pillarPromise]).then(function (results) {
    let screening = results[0];
    let tags = results[1];
    let pillars = results[2];

    console.log(screening)

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

    screening.save()

    res.status(200).send({
      message: "OK",
    });
  }).catch((err) => {
    res.status(500).send({
      message: err
    })
  })
};

module.exports = {
  create,
  update
};