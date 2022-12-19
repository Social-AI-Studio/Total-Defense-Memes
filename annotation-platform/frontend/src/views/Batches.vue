<template>
  <div class="mt-3">

    <b-container>
      <h4 align="center" class="mt-4 mb-4">Batch</h4>
      <b-row cols-md="4">
        <div v-for="batch in batches" :key="batch.id">
          <b-card
            border-variant="info"
            :header="batch.name"
            class="m-1"
            align="center">

            <b-card-text>
              <!-- <p>Progress: {{ ex.currentCount }} / {{ ex.totalCount }}</p> -->
            </b-card-text>

            <router-link
              :to="{ name: 'batch', params: { batchId: batch.id } }"
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
      batches: [],
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
        .get(`${Settings.PROTOCOL}://${Settings.HOST}:${Settings.PORT}/api/screening`, {
          headers: {
            "x-access-token": auth.getToken(),
          },
        })
        .catch((err) => {
          console.log(err);
        });

      this.loading = false;
      this.batches = res.data.batches;
      
    },
  },
};
</script>
