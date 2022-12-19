<template>
  <b-row>
    <screening-sidebar class="col-3" :key="sidebarIndex" v-bind:stageLoaded="loaded"
      v-bind:items="filterItems" v-bind:activeIndex="activeIndex" v-on:onItemChange="onItemChange"
      v-on:onFilterSelected="onFilterSelected"></screening-sidebar>

    <screening
      class="col-6"
      v-if="loaded"
      v-bind:item="item"
      v-on:onSaveClick="onSaveClick"
    ></screening>


    <br />
  </b-row>
</template>

<script>
import { Settings } from "../config/api.config";
import Screening from "../components/Screening.vue";
import ScreeningSidebar from "../components/sidebars/ScreeningSidebar.vue";
// import InfoBar from "../components/info/InfoBar.vue";
import auth from "../utils/auth";
import axios from "axios";
import moment from "moment-timezone";

export default {
  components: {
    screening: Screening,
    "screening-sidebar": ScreeningSidebar,
  },
  data() {
    return {
      loaded: false,

      stage: null,
      items: [],

      activeIndex: 0,
      sidebarIndex: 1,
      error: null,

      selected: "all"
    };
  },
  async created() {
    await this.fetchMemes();
  },
  computed: {
    filterItems: function () {
      if (this.selected == "pending") {
        return this.items.filter(this.isPending);
      }

      if (this.selected == "completed") {
        return this.items.filter(this.isComplete);
      }

      return this.items;
    },
    item: function () {
      if (this.filterItems.length > 0) {
        return this.filterItems[this.activeIndex];
      } else {
        return {};
      }
    },
  },
  methods: {
    async fetchMemes() {
      this.error = null;
      this.loaded = false;

      const batchId = this.$route.params.batchId;

      const res = await axios
        .get(
          `${Settings.PROTOCOL}://${Settings.HOST}:${Settings.PORT}/api/screening/${batchId}`,
          {
            headers: {
              "x-access-token": auth.getToken(),
            },
          }
        )
        .catch((err) => {
          console.log(err);
        });

      this.loaded = true;
      this.items = res.data.screenings;

      console.log(this.items)
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
    isComplete(item) {
      const createdAt = moment(item.createdAt).tz("Asia/Singapore");
      const updatedAt = moment(item.updatedAt).tz("Asia/Singapore");
      return !createdAt.isSame(updatedAt);
    },
    isPending(item) {
      const createdAt = moment(item.createdAt).tz("Asia/Singapore");
      const updatedAt = moment(item.updatedAt).tz("Asia/Singapore");
      return createdAt.isSame(updatedAt);
    },
    onItemChange(idx) {
      this.activeIndex = idx;
    },
    onSaveClick() {
      this.activeIndex++;
    },
    onFilterSelected(val) {
      console.log(val);
      this.selected = val;
    },
  },
};
</script>