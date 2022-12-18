<template>
  <a class="list-group-item list-group-item-action py-3 lh-tight"
    :class="{'complete': saveTime != 'Pending'}"
    v-on:click="$emit('onTabSelected', index)">
    <div class="d-flex w-100 align-items-center justify-content-between">
      <b-img
        thumbnail
        fluid
        :src="imagepath"
        class="img-thumbnail"
      ></b-img>
      <small>{{ saveTime }}</small>
    </div>
  </a>
</template>


<script>
import { Settings } from "../../config/api.config";
import moment from "moment-timezone";

export default {
  name: "image-sidebar-item",
  props: ["index", "item"],
  data() {
    return {
      imagepath: `${Settings.PROTOCOL}://${Settings.HOST}:${Settings.PORT}/${this.item.Meme.image}`,
    };
  },
  computed: {
    createdAt: function() {
        return moment(this.item.createdAt).tz("Asia/Singapore");
    },
    updatedAt: function() {
        return moment(this.item.updatedAt).tz("Asia/Singapore");
    },
    saveTime: function () {
      if (!this.createdAt.isSame(this.updatedAt)) {
        var currentTime = moment();
        if (this.updatedAt.isSame(currentTime, "day")) {
          var duration = moment.duration(currentTime.diff(this.updatedAt));
          var hours = Math.floor(duration.asHours(), 0);

          if (hours >= 1) return `(${hours} hours ago)`;
          else var minutes = Math.floor(duration.asMinutes(), 0);
          return `${minutes} minutes ago`;
        } else {
          return `${this.updatedAt.format("DD/MM h:mm:ss A")}`;
        }
      }

      return "Pending";
    },
  },
};
</script>

<style>
.img-thumbnail {
  max-width: 100px;
  max-height: 100px;
}

.complete {
  z-index: 2;
  color: #fff;
  background-color: #20c997;
  border-color: #20c997;
}

.sidebar.list-group-item-action:hover, .list-group-item-action:focus {
  background-color: #17a2b8 !important;
  border-color: #17a2b8 !important;
}

.list-group-item.active {
  background-color: #17a2b8 !important;
  border-color: #17a2b8 !important;
}
</style>