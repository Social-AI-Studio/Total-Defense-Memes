<template>
  <div>
    <b-card no-body class="mb-1">
      <b-card-header header-tag="header" class="p-1" role="tab">
        <b-button block v-b-toggle="'social-targets'" variant="info"
          >Established Social Targets</b-button
        >
      </b-card-header>
      <b-collapse id="social-targets" visible role="tabpanel">
        <b-card-body>
          <b-row cols="5">
            <b-button
              v-b-toggle="`${group}`"
              size="sm"
              v-for="(target, group) in targets"
              :key="target"
              >{{ group }}</b-button
            >
          </b-row>
          <b-collapse
            :id="group"
            class="mt-2"
            v-for="(target, group) in targets"
            :key="target"
          >
            <ul>
              <li v-for="t in target" :key="t">{{ t }}</li>
            </ul>
          </b-collapse>
        </b-card-body>
      </b-collapse>
    </b-card>

    <b-card no-body class="mb-1">
      <b-card-header header-tag="header" class="p-1" role="tab">
        <b-button block v-b-toggle="'others'" variant="info"
          >Other Information</b-button
        >
      </b-card-header>
      <b-collapse id="others" visible role="tabpanel">
        <b-card-body>
          <p style="margin: 0; padding: 0">
            <b>Best Guess Labels:</b> <br />
            {{ item.Meme.best_guess_labels }}
          </p>
          <br />

          <p style="margin: 0; padding: 0"><b>Entities Detected:</b></p>
          <ul>
            <li v-for="entity in item.Meme.entities" :key="entity">
              {{ entity }}
            </li>
          </ul>

          <p style="margin: 0; padding: 0"><b>Protected Category:</b></p>
          <ul
            v-if="protected_pc.length > 0"
            class="list-inline d-inline-block mb-2"
          >
            <li
              v-for="label in protected_pc"
              :key="label"
              class="list-inline-item"
            >
              <b-form-tag :title="label" variant="light">{{
                label
              }}</b-form-tag>
            </li>
          </ul>

          <p style="margin: 0; padding: 0"><b>Fine-Grain Labels:</b></p>
          <ul
            v-if="item.Meme.final_labels.length > 0"
            class="list-inline d-inline-block mb-2"
          >
            <li
              v-for="label in item.Meme.final_labels"
              :key="label"
              class="list-inline-item"
            >
              <b-form-tag :title="label" variant="light">{{
                label
              }}</b-form-tag>
            </li>
          </ul>
        </b-card-body>
      </b-collapse>
    </b-card>
  </div>
</template>


<script>
export default {
  name: "infobar",
  props: ["item", "targets"],
  data() {
    return {
      protected_pc: this.item.Meme.gold_pc.split(","),
    };
  },
};
</script>