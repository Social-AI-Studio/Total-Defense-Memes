<template>
  <div class="annotation p-1">
    <b-card :img-src="imagepath" img-top tag="article">
      <p style="margin: 0; padding: 0">
        <b>Best Guess Labels:</b> <br />
        {{ annotation.Meme.best_guess_labels }}
      </p>
      <br />

      <p style="margin: 0; padding: 0"><b>Entities Detected:</b></p>
      <ul>
        <li v-for="entity in annotation.Meme.entities" :key="entity">
          {{ entity }}
        </li>
      </ul>

      <p style="margin: 0; padding: 0"><b>Protected Category:</b></p>
      <ul
        v-if="protected_pc.length > 0"
        class="list-inline d-inline-block mb-2"
      >
        <li v-for="label in protected_pc" :key="label" class="list-inline-item">
          <b-form-tag :title="label" variant="light">{{ label }}</b-form-tag>
        </li>
      </ul>

      <p style="margin: 0; padding: 0"><b>Existing Labels:</b></p>
      <div v-for="(prelabel, index) in annotation.prelabels" :key="prelabel">
        <div class="container mb-3">
          <div class="row">
            <div class="col-1 p-0">[{{ index }}]</div>
            <div class="col-10 pl-1 pr-1">
              <ul class="list-inline d-inline-block mb-2">
                <li
                  v-for="label in prelabel"
                  :key="label"
                  class="list-inline-item"
                >
                  <b-form-tag :title="label" variant="light">{{
                    label
                  }}</b-form-tag>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <p style="margin: 0; padding: 0"><b>Annotator Labels:</b></p>
      <ul v-if="labels.length > 0" class="list-inline d-inline-block mb-2">
        <li v-for="label in labels" :key="label" class="list-inline-item">
          <b-form-tag
            @remove="removeTag(label)"
            :title="label"
            variant="info"
            >{{ label }}</b-form-tag
          >
        </li>
      </ul>

      <b-input-group>
        <template #prepend>
          <b-form-select
            id="category-select"
            v-model="currentCategory"
            :options="availableCategories"
          ></b-form-select>
        </template>
        <b-form-input
          v-model="search"
          id="tag-search-input"
          type="search"
          autocomplete="off"
        ></b-form-input>
      </b-input-group>

      <p class="mt-4 mb-1 p-0"><b>Remarks:</b></p>
      <b-input-group>
        <b-form-input
          v-model="remarks"
          id="remarks-input"
          autocomplete="off"
        ></b-form-input>
      </b-input-group>
      <p v-if="remarksError" class="error mt-0 pt-0">Do not leave your justifications blank!</p>

      <div
        v-if="availableOptions.length > 0"
        style="border: 1px solid rgba(0, 0, 0, 0.125)"
        class="mt-2"
      >
        <b-dropdown-item-button
          v-for="option in availableOptions"
          :key="option"
          style="list-style: none"
          @click="onOptionClick({ option, addTag })"
        >
          {{ option }}
        </b-dropdown-item-button>
      </div>

      <div class="mt-2" style="text-align: center">
        <b-button
          variant="info"
          v-if="saveTime != '(Unsaved)'"
          @click="onSaveButton()"
          >Save {{ saveTime }}
        </b-button>
        <b-button
          variant="warning"
          v-if="saveTime == '(Unsaved)'"
          @click="onSaveButton()"
          >Save {{ saveTime }}
        </b-button>
      </div>
    </b-card>
  </div>
</template>

<script>
import { Settings } from "../config/api.config";
import auth from "../utils/auth";
import axios from "axios";
import moment from "moment-timezone";

export default {
  name: "consolidation",
  props: ["annotation"],
  data() {
    return {
      imagepath: `${Settings.PROTOCOL}://${Settings.HOST}:${Settings.PORT}/${this.annotation.Meme.image}`,
      protected_pc: this.annotation.Meme.gold_pc.split(","),

      error: null,
      category: null,
      search: "",

      currentSearch: "",
      currentCategory: null,
      searchDesc: "",

      availableOptions: [],
      availableCategories: [
        { value: null, text: "All" },
        { value: "Gender", text: "Gender" },
        { value: "Race", text: "Race" },
        { value: "Religion", text: "Religion" },
        { value: "Nationality", text: "Nationality" },
        { value: "Disability", text: "Disability" },
        { value: "Neutral", text: "Neutral" },
      ],

      labels: this.annotation.labels,
      remarks: this.annotation.remarks,
      createdAt: moment(this.annotation.createdAt).tz("Asia/Singapore"),
      updatedAt: moment(this.annotation.updatedAt).tz("Asia/Singapore"),

      remarksError: false
    };
  },
  watch: {
    search: async function (val) {
      this.currentSearch = val.trim().toLowerCase();

      console.log(`currentSearch: ${this.currentSearch}`);
      if (this.currentSearch)
        this.getAvailableOptions(this.currentCategory, this.currentSearch);
      else this.availableOptions = [];
    },
    currentCategory: async function () {
      this.getAvailableOptions(this.currentCategory, this.currentSearch);
    },
  },
  computed: {
    saveTime: function () {
      if (this.labels.length !== 0 && !this.createdAt.isSame(this.updatedAt)) {
        var currentTime = moment();
        if (this.updatedAt.isSame(currentTime, "day")) {
          var duration = moment.duration(currentTime.diff(this.updatedAt));
          var hours = Math.floor(duration.asHours(), 0);

          if (hours >= 1) return `(${hours} hours ago)`;
          else var minutes = Math.floor(duration.asMinutes(), 0);
          return `(${minutes} minutes ago)`;
        } else {
          return `(${this.updatedAt.format("DD/MM h:mm:ss A")})`;
        }
      }

      return "(Unsaved)";
    },
  },
  methods: {
    onOptionClick({ option, addTag }) {
      addTag(option);
      this.search = "";
    },
    async onSaveButton() {
      if (this.remarks === "") {
        this.remarksError = true;
        return null
      } else {
        this.remarksError = false;
      }

      if (this.labels.length === 0) return null;

      const body = new URLSearchParams({
        memeId: this.annotation.id,
        labels: this.labels.join(","),
        remarks: this.remarks
      });

      const config = {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "x-access-token": auth.getToken(),
        },
      };

      const res = await axios
        .post(
          `${Settings.PROTOCOL}://${Settings.HOST}:${Settings.PORT}/api/memes/consolidation`,
          body.toString(),
          config
        )
        .catch((error) => {
          console.log(error);
        });

      if (res) {
        this.updatedAt = moment().tz("Asia/Singapore");
      }

      this.$emit("onSaveClick");
    },
    async getAvailableOptions(category, criteria) {
      console.log(criteria);
      console.log(category);
      if (criteria || category) {
        console.log("Calling");
        const res = await axios.get(
          `${Settings.PROTOCOL}://${Settings.HOST}:${Settings.PORT}/api/memes/categories?category=${category}&search=${criteria}`,
          {
            headers: { "x-access-token": auth.getToken() },
          }
        );

        var options = res.data;

        if (criteria) options.push(`Create new label: ${criteria}`);

        this.availableOptions = options;
      } else {
        console.log("Nah");
        // Show all options available
        this.availableOptions = [];
      }
    },
    addTag(option) {
      if (option.includes("Create new label")) {
        this.showModal(option.replace("Create new label: ", ""));
        return;
      }

      this.currentCategory = null;

      // Check for duplicates
      if (!this.labels.includes(option)) {
        this.labels.push(option);
      }
    },
    removeTag(option) {
      const index = this.labels.indexOf(option);
      this.labels.splice(index, 1);
    },
    showModal(subcategory) {
      this.$emit("onDialogClick", subcategory, this.addTag);
    },
  },
};
</script>

<style>
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


<style>
.error {
  color: red;
}
</style>
