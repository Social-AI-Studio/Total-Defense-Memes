<template>
  <div
    class="d-flex flex-column align-items-stretch flex-shrink-0 bg-white w-100"
  >
    <div v-if="stageLoaded" class="border p-1"> 
      <div class="d-flex w-100 align-items-center p-2">
        Show:
        <b-select
          v-model="selected"
          :options="options"
          size="sm"
          class="ml-2 mr-2"
          v-on:change="$emit('onFilterSelected', $event)"
        ></b-select>
      </div>

      <div class="wrapper">
        <b-list-group v-if="stageLoaded">
          <screening-sidebar-item
            :class="{ active: activeIndex === index }"
            v-for="(item, index) in items"
            :key="index"
            v-bind:index="index"
            v-bind:item="item"
            v-on:onTabSelected="$emit('onItemChange', index)"
          ></screening-sidebar-item>
        </b-list-group>
      </div>
    </div>
    <span v-else>Loading...</span>
  </div>
</template>


<script>
import { Settings } from "../../config/api.config";
import ScreeningSidebarItem from "./ScreeningSidebarItem.vue";

export default {
  name: "image-sidebar",
  props: ["stageLoaded", "items", "activeIndex"],
  components: {
    "screening-sidebar-item": ScreeningSidebarItem,
  },
  data() {
    return {
      selected: null,
      options: [
        { value: null, text: "All Items" },
        { value: "pending", text: "Pending Items" },
        { value: "completed", text: "Completed Items" },
      ],
    };
  },
  methods: {
    returnImageURL(imgPath) {
      return `${Settings.PROTOCOL}://${Settings.HOST}:${Settings.PORT}/${imgPath}`;
    },
  },
  directives: {
    scroll: {
      bind: function (el, binding) {
        let f = (evt) => {
          if (binding.value(evt, el)) {
            el.removeEventListener("scroll", f);
          }
        };

        el.addEventListener("scroll", f);
      },
    },
  },
};
</script>

<style>
.img-thumbnail {
  max-width: 100px;
  max-height: 100px;
}

.wrapper {
  overflow-y: auto;
  max-height: 70vh;
}
</style>
