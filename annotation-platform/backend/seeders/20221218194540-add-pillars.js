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

    const pillars = [
      "Military Defence", "Civil Defence", "Economic Defence", "Social Defence", 
      "Psychological Defence", "Digital Defence", "Others"
    ]
    var tagObjects =  []
    pillars.forEach(element => {
      tagObjects.push({
        "name": element,
        "createdAt": currentTime,
        "updatedAt": currentTime,
      })
    })

    await queryInterface.bulkInsert('Pillars', tagObjects, {});
  },

  async down (queryInterface, Sequelize) {
    /**
     * Add commands to revert seed here.
     *
     * Example:
     * await queryInterface.bulkDelete('People', null, {});
     */
    const pillars = [
      "Military Defence", "Civil Defence", "Economic Defence", "Social Defence", 
      "Psychological Defence", "Digital Defence", "Others"
    ]
    await queryInterface.bulkDelete('Pillars', pillars, {});
  }
};
