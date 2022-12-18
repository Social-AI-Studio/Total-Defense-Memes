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

    const tags = ["Singapore Armed Forces (SAF)", "National Day Parade (NDP)", "National Service (NS)", "Singapore Police Force (SPF)"]
    var tagObjects =  []
    tags.forEach(element => {
      tagObjects.push({
        "name": element,
        "createdAt": currentTime,
        "updatedAt": currentTime,
      })
    })

    await queryInterface.bulkInsert('Tags', tagObjects, {});
  },

  async down (queryInterface, Sequelize) {
    /**
     * Add commands to revert seed here.
     *
     * Example:
     * await queryInterface.bulkDelete('People', null, {});
     */
    const tags = ["Singapore Armed Forces (SAF)", "National Day Parade (NDP)", "National Service (NS)", "Singapore Police Force (SPF)"]
    await queryInterface.bulkDelete('Tags', tags, {});
  }
};
