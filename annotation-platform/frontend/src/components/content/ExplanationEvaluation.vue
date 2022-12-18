<template>
  <div>
    <b-img class="img-size" center :src="imagepath" alt="Center image"></b-img>

    <div>
      <p class="mt-4 mb-1 p-0"><b>Meme Characteristics:</b></p>

      <b-form-checkbox-group name="flavour-2" v-model="item.profanity">
        <b-form-checkbox value="sarcasm">Sarcasm</b-form-checkbox>
        <b-form-checkbox value="profanity">Profanity</b-form-checkbox>
      </b-form-checkbox-group>
    </div>

    <div
      v-for="(input, k) in item.Explanation.reasoning"
      :key="`reasoning-${k}`"
    >
      <p class="mt-4 mb-1 p-0">
        <b>Reasoning {{ k + 1 }}:</b>
      </p>
      <b-input-group>
        <b-form-textarea
          id="reasoning-input"
          v-model="input.reasoning"
          placeholder="Enter reasonings"
          rows="2"
          max-rows="3"
        ></b-form-textarea>
      </b-input-group>

      <p class="mt-4 mb-1 p-0">
        <b>Evaluation (For Reasoning {{ k + 1 }})</b>
      </p>

      <b-row cols-md="3" class="m-0">
        <div role="group">
          <label for="input-live">Fluent:</label>
          <b-form-input
            v-model="item.fluent[k]"
            placeholder="Enter value from 1 - 5"
          ></b-form-input>

          <p
            v-if="item.fluent[k] != '' && !assertWithinRange(item.fluent[k])"
            class="error mt-0 pt-0"
          >
            Rate the fluent from the scale of 1 - 5
          </p>
        </div>

        <div role="group">
          <label for="input-live">Relevant:</label>
          <b-form-input
            placeholder="Enter value from 1 - 5"
            v-model="item.relevant[k]"
          ></b-form-input>

          <p
            v-if="
              item.relevant[k] != '' && !assertWithinRange(item.relevant[k])
            "
            class="error mt-0 pt-0"
          >
            Rate the relevant from the scale of 1 - 5
          </p>
        </div>

        <div role="group">
          <label for="input-live">Complementary:</label>
          <b-form-input
            placeholder="Enter value from 1 - 5"
            v-model="item.complementary[k]"
          ></b-form-input>

          <p
            v-if="
              item.complementary[k] != '' &&
              !assertWithinRange(item.complementary[k])
            "
            class="error mt-0 pt-0"
          >
            Rate the complementary from the scale of 1 - 5
          </p>
        </div>
      </b-row>
    </div>

    <div>
      <p class="mt-4 mb-1 p-0 text-info">
        <b>Revised Reasoning</b>
      </p>
      <b-input-group>
        <b-form-textarea
          id="reasoning-input"
          v-model="item.remarks"
          placeholder="Enter revised reasonings (if applicable)"
          rows="2"
          max-rows="3"
        ></b-form-textarea>
      </b-input-group>
    </div>

    <div class="mt-2" style="text-align: center">
      <b-button variant="primary" @click="onSaveButton()">Submit</b-button>
    </div>
  </div>
</template>

<script>
import { Settings } from "../../config/api.config";
import auth from "../../utils/auth";
import axios from "axios";
import moment from "moment-timezone";

export default {
  name: "explanation",
  props: ["item", "targets", "itemLoaded"],
  data() {
    return {};
  },
  computed: {
    imagepath: function () {
      return `${Settings.PROTOCOL}://${Settings.HOST}:${Settings.PORT}/${this.item.Meme.image}`;
    },
  },
  methods: {
    assertWithinRange(val) {
      return val.match(/^[0-9]+$/) != null || (val > 0 && val < 6);
    },
    async onSaveButton() {
      // Check for errors
      var error = false;
      console.log(error);
      for (
        let index = 0;
        index < this.item.Explanation.reasoning.length;
        index++
      ) {
        const fluent = this.item.fluent[index];
        const relevant = this.item.relevant[index];
        const complementary = this.item.complementary[index];

        error =
          error ||
          !this.assertWithinRange(fluent) ||
          !this.assertWithinRange(relevant) ||
          !this.assertWithinRange(complementary);
      }

      console.log(error);

      if (error) return;

      if (this.item.profanity.includes("sarcasm")) {
        this.item.sarcasm = [];
        this.item.Explanation.reasoning.forEach(() => {
          this.item.sarcasm.push("true");
        });
      }

      if (this.item.profanity.includes("profanity")) {
        this.item.profanity = [];
        this.item.Explanation.reasoning.forEach(() => {
          this.item.profanity.push("true");
        });
      }

      const body = new URLSearchParams({
        id: this.item.id,
        fluent: JSON.stringify(this.item.fluent),
        relevant: JSON.stringify(this.item.relevant),
        complementary: JSON.stringify(this.item.complementary),
        profanity: JSON.stringify(this.item.profanity),
        sarcasm: JSON.stringify(this.item.sarcasm),
        remarks: this.item.remarks,
      });
      const config = {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "x-access-token": auth.getToken(),
        },
      };
      const res = await axios
        .post(
          `${Settings.PROTOCOL}://${Settings.HOST}:${Settings.PORT}/api/memes/explanationevaluation`,
          body.toString(),
          config
        )
        .catch((error) => {
          console.log(error);
        });
      if (res.status === 200) {
        this.item.updatedAt = moment().utc().format();
        this.$emit("onSaveClick");
      }
    },
  },
};
</script>

<style>
.img-size {
  max-width: 100%;
  max-height: 70vh;
}
</style>