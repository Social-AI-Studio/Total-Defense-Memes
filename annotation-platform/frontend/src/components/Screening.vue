<template>
  <div>
    <b-img class="img-size" center :src="imagepath" alt="Center image"></b-img>

    <p class="mt-4 mb-0 p-0"><b>Flag This Meme</b></p>
    <p class="mt-0 mb-2 p-0"><small>If you think this meme is too hard to annotate, you can flag this meme to (1)
        revisit at a later time and (2) inform us about it. <br /><em>IMPORTANT: You still have to submit the
          form</em></small></p>
    <div>
      <div class="form-check form-check-inline">
        <input class="form-check-input" type="checkbox" id="flaggingCheckbox" v-model="item.flagged">
        <label class="form-check-label" for="flaggingCheckbox">I'll think about this later!</label>
      </div>
    </div>

    <p class="mt-4 mb-0 p-0"><b>Content Type</b></p>
    <p class="mt-0 mb-2 p-0"><small>Do you regard the visual as a meme?</small></p>
    <div>
      <div class="form-check form-check-inline">
        <input class="form-check-input" type="radio" name="contentTypeOptions" id="memeRadio" value="1"
          v-model="item.contentType">
        <label class="form-check-label" for="memeRadio">Meme</label>
      </div>
      <div class="form-check form-check-inline">
        <input class="form-check-input" type="radio" name="contentTypeOptions" id="nonMemeRadio" value="0"
          v-model="item.contentType">
        <label class="form-check-label" for="nonMemeRadio">Non-Meme</label>
      </div>
    </div>

    <div v-if="item.contentType == 1">
      <p class="mt-4 mb-0 p-0"><b>Related Country</b></p>
      <p class="mt-0 mb-2 p-0"><small>Do you regard the visual as a Singapore meme?</small></p>
      <div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="relatedCountryOptions" id="sgRadio" value="1"
            v-model="item.relatedCountry">
          <label class="form-check-label" for="sgRadio">Singapore Meme</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="relatedCountryOptions" id="nonSGRadio" value="0"
            v-model="item.relatedCountry">
          <label class="form-check-label" for="nonSGRadio">Non-Singapore Meme</label>
        </div>
      </div>
    </div>

    <div v-if="(item.contentType == 1 && item.relatedCountry == 1)">
      <p class="mt-4 mb-1 p-0"><b>Text:</b></p>
      <b-input-group>
        <b-form-textarea id="remarks-input" v-model="item.text" rows="3" max-rows="100">{{ this.item.text
        }}</b-form-textarea>
      </b-input-group>

      <p class="mt-4 mb-0 p-0"><b>Defence Pillar(s)</b></p>
      <p class="mt-0 mb-2 p-0"><small>Would you classify this visual under any of the Total Defence Pillars?</small></p>
      <div>
        <div class="form-check" v-for="(pillar, idx) in pillars" :key="pillar">
          <input class="form-check-input" type="checkbox" :id="pillar" v-model="item.pillars" :value="idx">
          <label class="form-check-label" :for="pillar">{{ pillar }}</label>
        </div>
      </div>

      <p class="mt-4 mb-0 p-0"><b>Topic Tags</b></p>
      <p class="mt-0 mb-2 p-0"><small>The tags should capture all the essential elements being illustrated or mentioned
          in
          the meme.
        </small></p>
      <b-form-tags v-model="item.tags" no-outer-focus class="mb-2">
        <template v-slot="{ tags, inputAttrs, inputHandlers, tagVariant, addTag, removeTag }">
          <b-input-group class="mb-2">
            <b-form-input v-bind="inputAttrs" v-on="inputHandlers" placeholder="New tag - Press enter to add"
              class="form-control"></b-form-input>
            <b-input-group-append>
              <b-button @click="addTag()" variant="primary">Add</b-button>
            </b-input-group-append>
          </b-input-group>
          <div class="d-inline-block" style="font-size: 1.5rem;">
            <b-form-tag v-for="tag in tags" @remove="removeTag(tag)" :key="tag" :title="tag" :variant="tagVariant"
              class="mr-1">{{ tag }}</b-form-tag>
          </div>
        </template>
      </b-form-tags>

      <p class="mt-4 mb-0 p-0"><b>Stance</b></p>
      <p class="mt-0 mb-2 p-0"><small>Indicate whether the meme is against, neutral or supportive towards the identified
          pillars
        </small></p>
      <div class="mt-2 mb-2" v-for="p in item.pillars" :key="pillars[p]">
        {{ pillars[p] }}
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" :name="'stanceOptions' + p" value="1" :id="'againstRadio' + p"
            v-model="item.stance[p]">
          <label class="form-check-label" :for="'againstRadio' + p">Against</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" :name="'stanceOptions' + p" value="2" :id="'neutralRadio' + p"
            v-model="item.stance[p]">
          <label class="form-check-label" :for="'neutralRadio' + p">Neutral</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" :name="'stanceOptions' + p" value="3" :id="'supportRadio' + p"
            v-model="item.stance[p]">
          <label class="form-check-label" :for="'supportRadio' + p">Supportive</label>
        </div>
      </div>
    </div>

    <div class="mt-2" style="text-align: center">
      <b-button variant="primary" @click="onSaveButton()">Submit</b-button>
    </div>
  </div>
</template>

<script>
import { Settings } from "../config/api.config";
import auth from "../utils/auth";
import axios from "axios";
import moment from "moment-timezone";
// import TagsTypeAhead from "./Typeahead.vue";

export default {
  name: "explanation",
  props: ["item", "itemLoaded"],
  data() {
    return {
      // inputs: this.,
      errorNum: 0,

      pillars: ["Military Defence", "Civil Defence", "Economic Defence", "Social Defence",
        "Psychological Defence", "Digital Defence", "Others"],

      topictags: ["Singapore Armed Forces (SAF)", "Singapore Civil Defence Force (SCDF)"],

      // stance: [
      //   null, null, null, null, null, null, null
      // ],
    };
  },
  computed: {
    imagepath: function () {
      return `${Settings.PROTOCOL}://${Settings.HOST}:${Settings.PORT}/img/${this.item.filename}`;
    }
  },
  methods: {
    async createTag(tag) {

      const config = {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "x-access-token": auth.getToken(),
        },
      };

      const body = new URLSearchParams({
        tagName: tag,
      });

      const res = await axios
        .post(
          `${Settings.PROTOCOL}://${Settings.HOST}:${Settings.PORT}/api/tag/create`,
          body.toString(),
          config
        )
        .catch((error) => {
          console.log(error);
        });

      console.log(res.data.tagId)
      return res.data.tagId
    },
    async onSaveButton() {

      var msg = ""
      if (this.item.contentType == null) {
        msg += "Please decide whether this visual is a meme or non-meme\n"
      }

      if (this.item.relatedCountry == null) {
        msg += "Please decide whether this visual is a Singapore-related meme. \n"
      }

      if (msg != "") {
        alert(msg)
        return
      }

      const selectedPillars = [];
      const selectedStance = [];
      const tags = [];
      if (this.item.contentType == 1 && this.item.relatedCountry == 1) {
        // Create the tags
        for (let i = 0; i < this.item.tags.length; i++) {
          const element = this.item.tags[i];
          const tagId = await this.createTag(element)
          tags.push(tagId);
        }

        // Check whether the boxes are filled up
        for (let i = 0; i < this.item.pillars.length; i++) {
          selectedPillars.push(this.item.pillars[i] + 1)
        }

        for (let i = 0; i < this.item.pillars.length; i++) {
          const idx = this.item.pillars[i]
          if (this.item.stance[idx] != null) {
            selectedStance.push(this.item.stance[idx])
          }
        }

        if (tags.length == 0) {
          msg += "Please enter the appropriate tags\n"
        }

        if (selectedPillars.length == 0) {
          msg += "Please select the appropriate defence pillars\n"
        }

        if (selectedStance.length == 0 || selectedStance.length != selectedPillars.length) {
          msg += "Please select the stance for the corresponding pillars\n"
        }

        if (msg != "") {
          alert(msg);
          return
        }
      }

      const body = {
        contentType: this.item.contentType,
        relatedCountry: this.item.relatedCountry,
        topicTags: tags,
        pillars: selectedPillars,
        stance: selectedStance,
        flagged: this.item.flagged,
        text: this.item.text
      };

      const config = {
        headers: {
          // "Content-Type": "application/x-www-form-urlencoded",
          'Content-Type': 'application/json',
          "x-access-token": auth.getToken(),
        },
      };

      const res = await axios
        .put(
          `${Settings.PROTOCOL}://${Settings.HOST}:${Settings.PORT}/api/screening/${this.item.id}`,
          body,
          config
        )
        .catch((error) => {
          console.log(error);
        });

      console.log(res)

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


.bootstrap-tagsinput {
  width: 100%;
}

.label-info {
  background-color: #17a2b8;

}

.label {
  display: inline-block;
  padding: .25em .4em;
  font-size: 75%;
  font-weight: 700;
  line-height: 1;
  text-align: center;
  white-space: nowrap;
  vertical-align: baseline;
  border-radius: .25rem;
  transition: color .15s ease-in-out, background-color .15s ease-in-out,
    border-color .15s ease-in-out, box-shadow .15s ease-in-out;
}
</style>