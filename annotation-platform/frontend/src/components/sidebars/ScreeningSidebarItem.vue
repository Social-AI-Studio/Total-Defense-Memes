<template>
  <a class="list-group-item list-group-item-action py-3 lh-tight" :class="{ 'complete': status != 'Incompleted' }"
    v-on:click="$emit('onTabSelected', index)">
    <div class="d-flex w-100 align-items-center justify-content-between">
      <p>Image {{ index }}</p>
      <small>{{ status }}</small>
    </div>
  </a>
</template>


<script>
import moment from "moment-timezone";

export default {
  name: "image-sidebar-item",
  props: ["index", "item"],
  computed: {
    createdAt: function () {
      return moment(this.item.createdAt).tz("Asia/Singapore");
    },
    updatedAt: function () {
      return moment(this.item.updatedAt).tz("Asia/Singapore");
    },
    status: function () {
      if (!this.createdAt.isSame(this.updatedAt)) {
        return `${this.updatedAt.format("DD/MM h:mm:ss A")}`;
      }

      return "Incompleted";
    },
  },
};
</script>

<!-- <style>
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

.sidebar.list-group-item-action:hover,
.list-group-item-action:focus {
  background-color: #17a2b8 !important;
  border-color: #17a2b8 !important;
}

.list-group-item.active {
  background-color: #17a2b8 !important;
  border-color: #17a2b8 !important;
}
</style> -->