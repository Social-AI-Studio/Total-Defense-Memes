const db = require("../models");
const Batch = db.Batch;
const Meme = db.Meme;

const fs = require("fs");
const csv = require("fast-csv");

const upload = async (req, res) => {
  try {
    if (req.file == undefined) {
      return res.status(400).send("Please upload a CSV file!");
    }

    let batches = new Set();
    let memes = [];
    let path = __basedir + "/uploads/" + req.file.filename;

    fs.createReadStream(path)
      .pipe(csv.parse({ headers: true }))
      .on("error", (error) => {
        throw error.message;
      })
      .on("data", (row) => {
        batches.add(row['batch'])
        memes.push(row)
      })
      .on("end", () => {

        // Create batches
        var batchObjects = []
        batches.forEach(x => {
          batchObjects.push({
            "name": x
          })
        });

        Batch.bulkCreate(batchObjects).then((batches) => {

          // Remap batches
          var batch2Id = {}
          batches.forEach(element => {
            batch2Id[element.name] = element.id
          });

          // Update meme objects
          for (let i = 0; i < memes.length; i++) {
            const element = memes[i];
            element['batchId'] = batch2Id[element['batch']]
          }

          return Meme.bulkCreate(memes)
        }).then((memes) => {
          res.status(200).send({
            message:
              "Uploaded the file successfully: " + req.file.originalname,
          });
        }).catch((err) => {
          console.log(err)
          res.status(500).send({
            message: err,
          });
        })
      });
  } catch (error) {
    res.status(500).send({
      message: "Could not upload the file: " + req.file.originalname,
    });
  }
};

const getMemes = (req, res) => {
  Batch.findAll()
    .then((data) => {
      res.send(data);
    })
    .catch((err) => {
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving tutorials.",
      });
    });
};

module.exports = {
  upload,
  getMemes
};