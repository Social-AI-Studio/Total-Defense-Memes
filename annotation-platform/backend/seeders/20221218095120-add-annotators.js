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

    await queryInterface.bulkInsert('Users', [{
      username: "janelle",
      password: "Rum1001!",
      updatePassword: 0,
      createdAt: currentTime,
      updatedAt: currentTime
    },{
      username: "ed",
      password: "Rum1002!",
      updatePassword: 0,
      createdAt: currentTime,
      updatedAt: currentTime
    },{
      username: "andrew",
      password: "Rum1003!",
      updatePassword: 0,
      createdAt: currentTime,
      updatedAt: currentTime
    },{
      username: "angga",
      password: "Rum1004!",
      updatePassword: 0,
      createdAt: currentTime,
      updatedAt: currentTime
    },{
      username: "jianqing",
      password: "Rum1005!",
      updatePassword: 0,
      createdAt: currentTime,
      updatedAt: currentTime
    },{
      username: "shah",
      password: "Rum1006!",
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
