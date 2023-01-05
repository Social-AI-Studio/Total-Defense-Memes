const db = require("../models");
const Batch = db.Batch;
const Meme = db.Meme;
const Op = db.Sequelize.Op;

const fs = require("fs");
const csv = require("fast-csv");
const { assert } = require("console");

let NoNewMemesError = () => {
  var err = new Error();
  err.name = 'NoNewMemesError';
  return err;
};

const addMemesToBatch = async (req, res) => {
  try {
    if (req.file == undefined) {
      return res.status(400).send("Please upload a CSV file!");
    }

    let batches = new Set();
    let batchesType = new Set();
    let memes = [];
    let memeFilenames = [];
    let path = __basedir + "/uploads/" + req.file.filename;

    fs.createReadStream(path)
      .pipe(csv.parse({ headers: true }))
      .on("error", (error) => {
        throw error.message;
      })
      .on("data", (row) => {
        batches.add(row['batch'])
        batchesType.add(row['batchType'])
        memes.push(row)
        memeFilenames.push(row['filename'])
      })
      .on("end", async() => {

        console.log(batches)
        if (batches.size != 1) {
          var err = new Error();
          err.name = `More than one batch detected. Please upload csvs for individual batches separately.`;
          throw err;
        }

        // Find meme objects
        var memesPromises = Meme.findAll({
          where: {
            filename: {
              [Op.in]: memeFilenames
            }
          }
        })
        var batchPromise = Batch.findOrCreate({
          where: {
            "name": Array.from(batches)[0],
            "type": Array.from(batchesType)[0]
          }
        })

        Promise.all([memesPromises, batchPromise]).then(async (results) => {
          var memeObjs = results[0];
          var batchObj = results[1][0];
          console.log(`[AddMemeToBatch] Found Memes: ${memeObjs.length}`)
          console.log(batchObj.id)

          for (let i = 0; i < memeObjs.length; i++) {
            const element = memeObjs[i];

            // Remove found memes from the list
            var removedIdx = memeFilenames.indexOf(element.filename)
            memeFilenames.splice(removedIdx, 1);
            memes.splice(removedIdx, 1);

            // Create new MemeBatch for each existing memes
            element.addBatch(batchObj)
            await element.save()
          }

          if (memes.length == 0){
            throw NoNewMemesError();
          }

          // Create meme objects
          for (let i = 0; i < memes.length; i++) {
            const element = memes[i];
            element['batchId'] = 1 // batchId no longer in use
          }

          var memesPromises = Meme.bulkCreate(memes)
          var batchPromise = Batch.findOne({
            where: {
              "name": Array.from(batches)[0]
            }
          })

          return await Promise.all([memesPromises, batchPromise])

        }).then(async (results) => {
          var memeObjs = results[0];
          var batchObj = results[1];
          console.log(`[AddMemeToBatch] Created Memes: ${memeObjs.length}`)

          // Create new MemeBatch records
          for (let i = 0; i < memeObjs.length; i++) {
            const element = memeObjs[i];
            element.addBatch(batchObj)
            await element.save()
          }

          res.status(200).send({
            message: `new batch updated, ${memeObjs.length} new memes created`,
          });
        }).catch((err) => {
          console.log(err)
          
          if (err == "NoNewMemesError") {
            res.status(200).send({
              message: "new batch updated, no new memes created",
            });
          } else {
            res.status(500).send({
              message: err,
            });
          }
        })
      });
  } catch (error) {
    res.status(500).send({
      message: "Could not upload the file: " + req.file.originalname,
    });
  }
};

module.exports = {
  addMemesToBatch,
};