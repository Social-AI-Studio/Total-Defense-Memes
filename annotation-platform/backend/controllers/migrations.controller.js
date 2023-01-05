const db = require("../models");
const screeningpillarModel = require("../models/screeningpillar.model");

const Meme = db.Meme;
const MemeBatch = db.MemeBatch;
const Screening = db.Screening;

const Op = db.Sequelize.Op;

function migrateBatch(req, res) {
  MemeBatch.findAll().then((memeBatches) => {
    if (memeBatches.length > 0) {
      var err = new Error();
      err.name = "Table 'MemeBatch' is not empty";
      throw err;
    }

    return Meme.findAll()
  }).then((memes) => {

    var memeBatches = []
    for (let i = 0; i < memes.length; i++) {
      memeBatches.push({
        memeId: memes[i].id,
        batchId: memes[i].batchId,
      })
    }

    return MemeBatch.bulkCreate(memeBatches)
  }).then(() => {
    res.status(200).send({
      "msg": "OK"
    })
  }).catch((err) => {
    console.log(err)
    res.status(500).send({
      message: err
    })
  })
}


function migrateScreeningUpdated(req, res) {
  Screening.findAll({
    where: {
      updated: 0
    }
  }).then((screenings) => {
    if (screenings.length == 0) {
      var err = new Error();
      err.name = "All screenings has been completed";
      throw err;
    }

    var completedIds = []
    for (let i = 0; i < screenings.length; i++) {
      const element = screenings[i];

      var createdAt = Date.parse(element.createdAt)
      var updatedAt = Date.parse(element.updatedAt)

      if (updatedAt != createdAt) {
        completedIds.push(element.id)
      }
    }

    return Screening.update(
      { updated: 1 },
      {
        where: {
          id: completedIds
        },
      }
    )
  }).then(() => {
    res.status(200).send({
      "msg": "OK"
    })
  }).catch((err) => {
    console.log(err)
    res.status(500).send({
      message: err
    })
  })
}

module.exports = {
  migrateBatch,
  migrateScreeningUpdated
};