const db = require("../models");
const screeningpillarModel = require("../models/screeningpillar.model");

const Meme = db.Meme;
const Batch = db.Batch;
const MemeBatch = db.MemeBatch;

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

function migrateScreenings(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

module.exports = {
  migrateBatch,
  migrateScreenings
};