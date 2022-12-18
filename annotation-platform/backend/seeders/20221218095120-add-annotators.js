'use strict';

var bcrypt = require("bcryptjs");

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up (queryInterface, Sequelize) {
    /**
     * Add seed commands here.
     *
     * Example:
     * await queryInterface.bulkInsert('People', [{
     *   name: 'John Doe',
     *   isBetaMember: false
     * }], {});
    */
    const currentTime = new Date(new Date().toUTCString()).toISOString();

    await queryInterface.bulkInsert('Users', [{
      username: "janelle",
      password: bcrypt.hashSync("Rum1001!", 8),
      updatePassword: 0,
      createdAt: currentTime,
      updatedAt: currentTime
    },{
      username: "ed",
      password: bcrypt.hashSync("Rum1002!", 8),
      updatePassword: 0,
      createdAt: currentTime,
      updatedAt: currentTime
    },{
      username: "andrew",
      password: bcrypt.hashSync("Rum1003!", 8),
      updatePassword: 0,
      createdAt: currentTime,
      updatedAt: currentTime
    },{
      username: "angga",
      password: bcrypt.hashSync("Rum1004!", 8),
      updatePassword: 0,
      createdAt: currentTime,
      updatedAt: currentTime
    },{
      username: "jianqing",
      password: bcrypt.hashSync("Rum1005!", 8),
      updatePassword: 0,
      createdAt: currentTime,
      updatedAt: currentTime
    },{
      username: "shah",
      password: bcrypt.hashSync("Rum1006!", 8),
      updatePassword: 0,
      createdAt: currentTime,
      updatedAt: currentTime
    }], {});
  },

  async down (queryInterface, Sequelize) {
    /**
     * Add commands to revert seed here.
     *
     * Example:
     * await queryInterface.bulkDelete('People', null, {});
     */
    await queryInterface.bulkDelete('Users', [{
      username: "janelle"
    },{
      username: "ed"
    },{
      username: "andrew"
    },{
      username: "angga"
    },{
      username: "jianqing"
    },{
      username: "shah"
    }], {});
  }
};
