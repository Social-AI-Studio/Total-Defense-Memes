const db = require("../models");

const Tag = db.Tag;
const Op = db.Sequelize.Op;

const create = async (req, res) => {
  // Fetch the memes within the indicated batch
  Tag.create({
    name: req.body.tagName,
    annotatorId: req.userId
  }).then(() => {
    res.status(200).send({
      message:"OK",
    });
  }).catch((err) => {
    res.status(500).send({
      message: err
    })
  })
};

const fetch = async (req, res) => {
  // Fetch the memes within the indicated batch
  Tag.findAll({
    where: {
      name: {
        [Op.like]: '%' + req.body.query + '%'
      },
      annotatorId: req.userId
    }
  }).then((tags) => {
    res.status(200).send({
      tags: tags,
    });
  }).catch((err) => {
    res.status(500).send({
      message: err
    })
  })
};

module.exports = {
  create,
  fetch
};