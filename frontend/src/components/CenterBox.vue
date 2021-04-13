<template>
  <div
    v-if="currentTender"
    class="d-flex flex-column h-100"
  >
    <h3 class="text-center mt-2">
      Tender {{ currentTender.datestr }} {{ currentTender.market }}
      <b-icon :icon="arrowIcon(currentTender.direction)" :variant="arrowVariant(currentTender.direction)"></b-icon>{{ currentTender.tender_round }}
    </h3>
    <div class="d-flex flex-column flex-grow overflow-hidden">
      <b-pagination
        v-model="centerRound"
        :total-rows="currentRound - 1"
        per-page="1"
        limit="10" 
        first-number
        last-number
        align="center"
        class="my-2"
      ></b-pagination>
      <ResultTable :centerRound="centerRound" /> 
    </div>

  </div>
</template>


<script>
import ResultTable from "./ResultTable.vue"
import RoundUploader from "./RoundUploader.vue"

export default {
  components: {
    ResultTable,
    RoundUploader
  },
  data() {
    return {
      centerRound: 1
    }
  },
  methods: {
    arrowIcon(direction) {
      return direction == "U" ? "caret-up-fill" : "caret-down-fill"
    },
    arrowVariant(direction) {
      return direction == "U" ? "success" : "danger"
    }
  },
  computed: {
    currentTender() {
      return this.$store.getters.CurrentTender;
    },
    currentRound() {
      return this.currentTender.current_bid_round; 
    }
  }
}
</script>


<style>

.flex-grow {
  flex: 1;
}

</style>