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

    await queryInterface.bulkInsert('Users', [{
      username: "mshee",
      password: "Rum1005844!",
      updatePassword: 0,
      createdAt: currentTime,
      updatedAt: currentTime
    },{
      username: "nirmal",
      password: "Rum03408!",
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
