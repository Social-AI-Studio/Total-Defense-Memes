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

    await queryInterface.bulkInsert('Roles', [{
      name: "admin",
      createdAt: currentTime,
      updatedAt: currentTime
    }, {
      name: "annotator",
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
    await queryInterface.bulkDelete('Roles', [{
      name: "annotator"
    }, {
      name: "admin"
    }], {});
  }
};
