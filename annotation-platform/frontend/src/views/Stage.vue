<template>
  <div class="mt-3">

    <b-container>
      <h4 align="center" class="mt-4 mb-4">Explanations</h4>
      <b-row cols-md="4">
        <div v-for="ex in explanations" :key="ex.id">
          <b-card
            border-variant="info"
            :header="ex.name"
            class="m-1"
            align="center">
            <b-card-text>
              <p>Progress: {{ ex.currentCount }} / {{ ex.totalCount }}</p>
            </b-card-text>

            <router-link
              :to="{ name: 'explanations', params: { stageId: ex.id } }"
            >
              <b-button variant="info">Start!</b-button>
            </router-link>
          </b-card>
        </div>
      </b-row>

      <h4 align="center" class="mt-4 mb-4">Evaluations</h4>
      <b-row cols-md="4">
        <div v-for="ex in evaluations" :key="ex.id">
          <b-card
            border-variant="info"
            :header="ex.name"
            class="m-1"
            align="center"
          >
            <b-card-text>
              <p>Progress: {{ ex.currentCount }} / {{ ex.totalCount }}</p>
            </b-card-text>

            <router-link
              :to="{ name: 'explanationevaluations', params: { stageId: ex.id } }"
            >
              <b-button variant="info">Start!</b-button>
            </router-link>
          </b-card>
        </div>
      </b-row>
    </b-container>
  </div>
</template>
<script>
import { Settings } from "../config/api.config";
import auth from "../utils/auth";
import axios from "axios";

export default {
  data() {
    return {
      annotations: [],
      checks: [],
      consolidations: [],
      explanations: [],
      evaluations: [],
    };
  },
  created() {
    this.fetchStages();
  },
  methods: {
    async fetchStages() {
      this.error = this.taskList = null;
      this.loading = true;

      const res = await axios
        .get(`${Settings.PROTOCOL}://${Settings.HOST}:${Settings.PORT}/api/memes/stages`, {
          headers: {
            "x-access-token": auth.getToken(),
          },
        })
        .catch((err) => {
          console.log(err);
        });

      this.loading = false;

      this.annotations = res.data.filter(e => e.PhaseId === 1);
      this.checks = res.data.filter(e => e.PhaseId === 2);
      this.consolidations = res.data.filter(e => e.PhaseId === 3);
      this.explanations = res.data.filter(e => e.PhaseId === 4);
      this.evaluations = res.data.filter(e => e.PhaseId === 5);
      console.log(this.evaluations);
    },
  },
};
</script>
