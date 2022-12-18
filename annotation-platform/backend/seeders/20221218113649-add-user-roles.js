'use strict';

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

    var userRoles = [{
      userId: 1,
      roleId: 1,
      createdAt: currentTime,
      updatedAt: currentTime
    },{
      userId: 2,
      roleId: 1,
      createdAt: currentTime,
      updatedAt: currentTime
    },{
      userId: 1,
      roleId: 2,
      createdAt: currentTime,
      updatedAt: currentTime
    },{
      userId: 2,
      roleId: 2,
      createdAt: currentTime,
      updatedAt: currentTime
    },{
      userId: 3,
      roleId: 2,
      createdAt: currentTime,
      updatedAt: currentTime
    },{
      userId: 4,
      roleId: 2,
      createdAt: currentTime,
      updatedAt: currentTime
    },{
      userId: 5,
      roleId: 2,
      createdAt: currentTime,
      updatedAt: currentTime
    },{
      userId: 6,
      roleId: 2,
      createdAt: currentTime,
      updatedAt: currentTime
    },{
      userId: 7,
      roleId: 2,
      createdAt: currentTime,
      updatedAt: currentTime
    },{
      userId: 8,
      roleId: 2,
      createdAt: currentTime,
      updatedAt: currentTime
    }]

    await queryInterface.bulkInsert('UserRoles', userRoles, {});
  },

  async down (queryInterface, Sequelize) {
    /**
     * Add commands to revert seed here.
     *
     * Example:
     * await queryInterface.bulkDelete('People', null, {});
     */
    var userRoles = [{
      userId: 1,
      roleId: 1,
    },{
      userId: 2,
      roleId: 1,
    },{
      userId: 1,
      roleId: 2,
    },{
      userId: 2,
      roleId: 2,
    },{
      userId: 3,
      roleId: 2,
    },{
      userId: 4,
      roleId: 2,
    },{
      userId: 5,
      roleId: 2,
    },{
      userId: 6,
      roleId: 2,
    },{
      userId: 7,
      roleId: 2,
    },{
      userId: 8,
      roleId: 2,
    }]

    await queryInterface.bulkDelete('UserRoles', userRoles, {});
  }
};
