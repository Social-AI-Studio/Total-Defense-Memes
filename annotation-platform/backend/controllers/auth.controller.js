const db = require("../models");
const config = require("../config/auth.config");
const User = db.User;
const Role = db.Role;

const Op = db.Sequelize.Op;

var jwt = require("jsonwebtoken");
var bcrypt = require("bcryptjs");

exports.signup = (req, res) => {
  // Save User to Database
  User.create({
    username: req.body.username,
    email: req.body.email,
    password: bcrypt.hashSync(req.body.password, 8)
  })
    .then(user => {
      if (req.body.roles) {
        Role.findAll({
          where: {
            name: {
              [Op.or]: req.body.roles
            }
          }
        }).then(roles => {
          user.setRoles(roles).then(() => {
            res.send({ message: "User registered successfully!" });
          });
        });
      } else {
        // user role = 1
        user.setRoles([1]).then(() => {
          res.send({ message: "User registered successfully!" });
        });
      }
    })
    .catch(err => {
      res.status(500).send({ message: err.message });
    });
};

exports.signin = (req, res) => {
  var content = {}

  User.findOne({
    where: {
      username: req.body.username
    }
  }).then(user => {
    if (!user) {
      return Promise.reject({
        status_code: 404,
        message: "User Not Found"
      })
    }

    var passwordIsValid = bcrypt.compareSync(
      req.body.password,
      user.password
    );

    if (!passwordIsValid) {
      return Promise.reject({
        status_code: 401,
        message: "Invalid Password!"
      })
    }

    // Count the number of annotations performed
    content.id = user.id
    content.username = user.username
    content.email = user.email
    content.accessToken = jwt.sign({ id: user.id }, config.secret, {
      expiresIn: 86400 // 24 hours
    });

    return user.getRoles()
  }).then((roles) => {
    var authorities = [];
    for (let i = 0; i < roles.length; i++) {
      authorities.push("ROLE_" + roles[i].name.toUpperCase());
    }

    content.authorities = authorities
    res.status(200).send(content)
  }).catch(err => {
    res.status(err.status_code).send({ message: err.message });
  });
};
