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
  var userPromise = User.findByPk(req.body.annotatorId)

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
        memeId: element.id,
        text: element.text
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

let getBreakChainError = () => {
  let err = new Error();
  err.name = 'BreakChainError';
  return err;
};

const update = async (req, res) => {

  // Fetch the memes within the indicated batch

  Screening.findOne({
    where: {
      id: req.params.screeningId,
    }
  }).then(async function (screening) {

    // Update screening
    screening.contentType = req.body.contentType;
    screening.flagged = req.body.flagged;

    if (screening.contentType == 1) {
      screening.relatedCountry = req.body.relatedCountry;
    }

    if ((screening.contentType == 0) || (screening.relatedCountry == 0)) {
      res.status(200).send({message: "OK"})
      throw getBreakChainError();
    }

    const screeningPromise = Screening.findOne({
      where: {
        id: req.params.screeningId,
      }
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

    return Promise.all([screeningPromise, tagPromise, pillarPromise])

  }).then(async function (results) {
    let screening = results[0];
    let tags = results[1];
    let pillars = results[2];

    // Save Text
    screening.text = req.body.text

    if (screening.relatedCountry) {
      screening.removePillars(screening.Pillars)
      for (let i = 0; i < pillars.length; i++) {
        const element = pillars[i];
        screening.addPillar(element, { through: { stance: req.body.stance[i] } })
      }

      screening.setTags(tags)
    }

    await screening.save()

    res.status(200).send({
      message: "OK",
    });
  // }).catch((err) => {
  //   if (err != "BreakChainError") {
  //     res.status(500).send({
  //       message: err
  //     })
  //   }
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
      where: { batchId: req.params.batchId },
      required: true,
      as: "memes"
    }]
  }).then((screenings) => {
    res.status(200).send({
      screenings: screenings,
    });
  })
};

const fetchAll = async (req, res) => {

  // Fetch the memes within the indicated batch
  const response = []
  User.findByPk(req.userId, {
    include: [{
      model: Batch, as: "batches"
    }]
  }).then((user) => {

    // Prep outputs
    var currentPromises = []
    var totalPromises = []
    for (let i = 0; i < user.batches.length; i++) {
      const batch = user.batches[i];
      response.push({
        "id": batch.id,
        "name": batch.name
      })
    }

    res.status(200).send({
      "batches": response
    })
  });


  //     // Get existing and total counts
  //     currentPromises.push(
  //       Screening.count({
  //         where: {
  //           annotatorId: req.userId,
  //           contentType: {
  //             [Op.ne]: null
  //           }
  //         },
  //         include: [{
  //           model: Meme,
  //           where: { batchId: batch.id },
  //           required: true,
  //           as: "memes"
  //         }]
  //       })
  //     )
  //     totalPromises.push(
  //       Screening.count({
  //         where: {
  //           annotatorId: req.userId
  //         },
  //         include: [{
  //           model: Meme,
  //           where: { batchId: batch.id },
  //           required: true,
  //           as: "memes"
  //         }]
  //       }))
  //   }

  //   console.log(currentPromises.length)

  //   return Promise.all(currentPromises, totalPromises)
  // }).then((results) => {
  //   var currentCounts = results[0]
  //   var totalCounts = results[1]

  //   console.log(currentCounts)
  //   console.log(totalCounts)

  //   for (let i = 0; i < currentCounts.length; i++) {
  //     response[i]['current'] = currentCounts[i];
  //     response[i]['total'] = totalCounts[i];
  //   }

  //   res.status(200).send({
  //     "data": response
  // })
  // })
};

module.exports = {
  create,
  update,
  fetch,
  fetchAll
};