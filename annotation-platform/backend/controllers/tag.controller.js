const db = require("../models");

const Tag = db.Tag;
const Op = db.Sequelize.Op;

const create = async (req, res) => {
  // Fetch the memes within the indicated batch
  Tag.findOne({
    where: {
      name: req.body.tagName,
      annotatorId: req.userId
    }
  }).then((tag) => {
    if (tag != null) {
      let error = new Error();
      error.name = tag.id;
      throw error
    }

    return Tag.create({
      name: req.body.tagName,
      annotatorId: req.userId
    })
  }).then((tag) => {
    res.status(200).send({
      message: "Tag created!",
      tagId: tag.id
    });
  }).catch((err) => {
    res.status(200).send({
      message: "Tag already exists",
      tagId: err.name
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