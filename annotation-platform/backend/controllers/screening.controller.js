const db = require("../models");

const Meme = db.Meme;
const Batch = db.Batch;
const Screening = db.Screening;

const create = async (req, res) => {

  // Fetch the memes within the indicated batch
  Batch.findOne({
    where: {
      name: req.body.batchName
    },
    include: [{
      model:Meme, as: "memes"
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
      message:"OK",
    });
  })
};

const update = async (req, res) => {

  // Fetch the memes within the indicated batch
  console.log(req.body.screeningId)
  Screening.findOne({
    where: {
      annotatorId: req.body.annotatorId,
      memeId: req.body.memeId
    }
  }).then((screening) => {
    console.log(screening)
    // Create screenings
    screening.contentType = req.body.contentType;
    screening.relatedCountry = req.body.relatedCountry;
    screening.flagged = req.body.flagged;

    console.log(screening)
    return screening.save()
  }).then((screening) => {
    console.log(screening) 
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