'use strict';

var bcrypt = require("bcryptjs");

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
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
      username: "mshee",
      password: bcrypt.hashSync("Rum1005844!", 8),
      updatePassword: 0,
      createdAt: currentTime,
      updatedAt: currentTime
    },{
      username: "nirmal",
      password: bcrypt.hashSync("Rum03408!", 8),
      updatePassword: 0,
      createdAt: currentTime,
      updatedAt: currentTime
    }], {});
  },

  async down(queryInterface, Sequelize) {
    /**
     * Add commands to revert seed here.
     *
     * Example:
     * await queryInterface.bulkDelete('People', null, {});
     */
    await queryInterface.bulkDelete('Users', [{
      username: "mshee"
    },{
      username: "nirmal"
    }], {});
  }
};
