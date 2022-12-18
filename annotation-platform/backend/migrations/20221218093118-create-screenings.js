'use strict';

const { INTEGER } = require('sequelize');

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('Screenings', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      memeId: {
        type: Sequelize.INTEGER,
        references: {
          model: 'Memes', // name of Target model
          key: 'id', // key in Target model that we're referencing
        },
        onUpdate: 'CASCADE',
        onDelete: 'CASCADE',
      },
      annotatorId: {
        type: Sequelize.INTEGER,
        references: {
          model: 'Users', // name of Target model
          key: 'id', // key in Target model that we're referencing
        },
        onUpdate: 'CASCADE',
        onDelete: 'CASCADE',
      },
      contentType: {
        type: Sequelize.INTEGER
      },
      relatedCountry: {
        type: Sequelize.INTEGER
      },
      flagged: {
        type: Sequelize.INTEGER,
        defaultValue: 0,
      },
      visibility: {
        type: Sequelize.INTEGER,
        defaultValue: 0,
      },
      createdAt: {
        allowNull: false,
        type: Sequelize.DATE
      },
      updatedAt: {
        allowNull: false,
        type: Sequelize.DATE
      }
    }).then(() => queryInterface.addIndex('Screenings', {
      fields: ['annotatorId', 'memeId'],
      unique: true
    }));
  },
  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('Screenings');
  }
};