const db = require("../models");
const Annotation = db.Annotation;
const Meme = db.Meme;
const Stage = db.Stage;
const Op = db.Sequelize.Op;

var jwt = require("jsonwebtoken");
var bcrypt = require("bcryptjs");

exports.getAnnotations = (req, res) => {
    Annotation.findAll({
        where: {
            UserId: req.userId,
            StageId: req.query.stage
        },
        include: [
            { model: Meme }
        ],
        offset: req.query.offset,
        limit: req.query.limit,
        order: [
            ['id', 'ASC']
        ]
    }).then(annotations => {
        for (let index = 0; index < annotations.length; index++) {
            const label = annotations[index].dataValues.labels
            const meme = annotations[index].dataValues.Meme.dataValues

            if (label == null) {
                annotations[index].dataValues.labels = []
            } else {
                annotations[index].dataValues.labels = label.split(',')
            }

            annotations[index].dataValues.Meme.dataValues.entities = meme.entities.split(',')
            annotations[index].dataValues.Meme.dataValues.automated_labels = meme.automated_labels.split(',')
        }

        res.status(200).send(annotations);
    }).catch(err => {
        res.status(500).send({ message: err.message });
    });
};

exports.saveAnnotation = (req, res) => {
    Annotation.update({
        labels: req.body.labels
    }, {
        where: {
            id: req.body.memeId,
            userId: req.userId
        }
    }).then(result => {
        if (result == 1)
            res.status(200).send({ message: `Annotation ${req.body.memeId} updated` });
        else
            res.status(500).send({ message: `Annotation ${req.body.memeId} not found` });
    }).catch(err => {
        res.status(500).send({ message: err.message });
    });
};