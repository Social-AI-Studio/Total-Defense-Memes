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
  }).then((screenings) => { 
    res.status(200).send({
      message:"OK",
    });
  })

  // Screening.create({
  //   annotatorId: req.body.annotatorId,
  //   memeId: req.body.memeId,
  // })

  // fs.createReadStream(path)
  //   .pipe(csv.parse({ headers: true }))
  //   .on("error", (error) => {
  //     throw error.message;
  //   })
  //   .on("data", (row) => {
  //     batches.add(row['batch'])
  //     memes.push(row)
  //   })
  //   .on("end", () => {

  //     // Create batches
  //     var batchObjects = []
  //     batches.forEach(x => {
  //       batchObjects.push({
  //         "name": x
  //       })
  //     });

  //     Batch.bulkCreate(batchObjects).then((batches) => {

  //       // Remap batches
  //       var batch2Id = {}
  //       batches.forEach(element => {
  //         batch2Id[element.name] = element.id
  //       });

  //       // Update meme objects
  //       for (let i = 0; i < memes.length; i++) {
  //         const element = memes[i];
  //         element['batchId'] = batch2Id[element['batch']]
  //       }

  //       return Meme.bulkCreate(memes)
  //     }).then((memes) => {
  //       res.status(200).send({
  //         message:
  //           "Uploaded the file successfully: " + req.file.originalname,
  //       });
  //     }).catch((err) => {
  //       console.log(err)
  //       res.status(500).send({
  //         message: err,
  //       });
  //     })
  //   });
};

module.exports = {
  create
};