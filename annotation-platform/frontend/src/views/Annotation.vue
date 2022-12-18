<template>
  <div class="annotation mb-2 mt-2">
    <div class="loading" v-if="loading">Loading...</div>
    <div v-if="error" class="error">
      {{ error }}
    </div>
    <div align="center">
      <span><b>{{this.stage}}</b></span> <br>
      {{this.currCount}} / {{this.totalCount}}
    </div>
    <br>
    <b-container>

      <b-row cols-md="3">
        <meme
          v-for="annotation in annotationList"
          :key="annotation.id"
          v-bind:annotation="annotation"
          v-on:onDialogClick="onDialogClick"
          v-on:onSaveClick="onSaveClick"
        ></meme>
      </b-row>

      <div class="mt-3">
        <b-pagination
          v-model="currentPage"
          :total-rows="totalCount"
          align="center"
          per-page="9"
          hide-goto-end-buttons
          last-number
        ></b-pagination>
      </div>
      
    </b-container>

    <b-modal
      id="creation-modal"
      ref="modal"
      title="Create New Subcategory"
      @hidden="resetModal"
      @ok="handleOk"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit">
        <label for="sb-locales">Category</label>
        <b-form-select
          id="sb-locales"
          v-model="createCategory"
          :options="availableCategories"
        ></b-form-select>
        <div
          v-if="!createCategoryState"
          tabindex="-1"
          role="alert"
          aria-live="assertive"
          aria-atomic="true"
          class="d-block invalid-feedback"
          id="__BVID__41__BV_feedback_invalid_"
        >
          category is required
        </div>

        <b-form-group
          class="mt-2"
          label="Subcategory"
          label-for="subcategory-input"
          invalid-feedback="subcategory is required"
          :state="createSubcategoryState"
        >
          <b-form-input
            id="subcategory-input"
            v-model="createSubcategory"
            :state="createSubcategoryState"
            required
          ></b-form-input>
        </b-form-group>
      </form>
    </b-modal>
  </div>
</template>

<script>
import { Settings } from "../config/api.config";
import Meme from "../components/Meme.vue";
import auth from "../utils/auth";
import axios from "axios";

export default {
  components: {
    meme: Meme,
  },
  data() {
    return {
      stage: "",
      currCount: 0,
      totalCount: 1,

      currentPage: 1,
      limit: 9,

      loading: false,
      post: null,
      error: null,

      createCategory: null,
      createSubcategory: "",
      createCategoryState: null,
      createSubcategoryState: null,

      availableCategories: [
        { value: null, text: "None" },
        { value: "Gender", text: "Gender" },
        { value: "Race", text: "Race" },
        { value: "Religion", text: "Religion" },
        { value: "Nationality", text: "Nationality" },
        { value: "Disability", text: "Disability" },
      ],
    };
  },
  async created() {
    await this.fetchStage();
    await this.fetchMemes();
  },
  watch: {
    currentPage: async function () {
      await this.fetchMemes();
    },
  },
  methods: {
    async fetchMemes() {
      this.error = this.annotationList = null;
      this.loading = true;

      const offset = (this.currentPage - 1) * this.limit;
      const stageId = this.$route.params.stageId;

      const res = await axios
        .get(
          `${Settings.PROTOCOL}://${Settings.HOST}:${Settings.PORT}/api/memes/annotations?offset=${offset}&limit=${this.limit}&stage=${stageId}`,
          {
            headers: {
              "x-access-token": auth.getToken(),
            },
          }
        )
        .catch((err) => {
          console.log(err);
        });

      console.log(res)
      this.loading = false;
      this.annotationList = res.data;
    },
    async fetchStage() {
      this.error = this.stage = null;
      this.loading = true;

      const stageId = this.$route.params.stageId;

      const res = await axios
        .get(
          `${Settings.PROTOCOL}://${Settings.HOST}:${Settings.PORT}/api/memes/stage?stage=${stageId}`,
          {
            headers: {
              "x-access-token": auth.getToken(),
            },
          }
        )
        .catch((err) => {
          console.log(err);
        });

      this.loading = false;
      this.stage = res.data.name;
      this.currCount = res.data.currentCount;
      this.totalCount = res.data.totalCount;
    },
    resetModal() {
      this.createCategory = null;
      // (this.createCategoryState = null), (this.createSubcategory = "");
      this.createSubcategoryState = null;
    },
    handleOk(bvModalEvt) {
      // Prevent modal from closing
      bvModalEvt.preventDefault();
      // Trigger submit handler
      this.handleSubmit();
    },
    async handleSubmit() {
      // Exit when the form isn't valid
      if (!this.checkFormValidity()) {
        return;
      }

      const body = new URLSearchParams({
        category: this.createCategory,
        subcategory: this.createSubcategory,
      });

      const config = {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "x-access-token": auth.getToken(),
        },
      };

      const res = await axios
        .post(
          `${Settings.PROTOCOL}://${Settings.HOST}:${Settings.PORT}/api/memes/category`,
          body.toString(),
          config
        )
        .catch((error) => {
          console.log(error);
        });

      console.log(res);

      if (res.status == 200) {
        this.modalCallback(
          `[${this.createCategory}] ${this.createSubcategory}`
        );
      }

      // Push the name to submitted names
      // this.submittedNames.push(this.name);
      // Hide the modal manually
      this.$nextTick(() => {
        this.$bvModal.hide("creation-modal");
      });
    },
    checkFormValidity() {
      const categoryValid = this.createCategory != null;
      const subcategoryValid = this.$refs.form.checkValidity();
      this.createSubcategoryState = subcategoryValid;

      return subcategoryValid && categoryValid;
    },
    onDialogClick(subcategory, cb) {
      this.createSubcategory = subcategory;
      this.modalCallback = cb;
      this.$bvModal.show("creation-modal");
    },
    onSaveClick() {
      this.currCount += 1;
    },
  },
};
</script>

<style>
.loading {
  position: absolute;
  top: 10px;
  right: 10px;
}
.error {
  color: red;
}
.content {
  transition: all 0.35s ease;
  position: absolute;
}
.slide-enter {
  opacity: 0;
  transform: translate(30px, 0);
}
.slide-leave-active {
  opacity: 0;
  transform: translate(-30px, 0);
}
</style>