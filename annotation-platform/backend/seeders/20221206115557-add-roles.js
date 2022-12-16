'use strict';

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

    await queryInterface.bulkInsert('Role', [{
      name: "Annotator",
      createdAt: currentTime,
      updatedAt: currentTime
    }, {
      name: "Administrator",
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
    await queryInterface.bulkDelete('Role', [{
      name: "Annotator"
    }, {
      name: "Administrator"
    }], {});
  }
};
