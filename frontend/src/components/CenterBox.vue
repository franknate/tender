<template>
  <div
    v-if="currentTender"
    class="d-flex flex-column h-100"
  >
    <h2 class="text-center mt-2">
      Tender {{ currentTender.datestr }} {{ currentTender.market }} {{ currentTender.direction }}-{{ currentTender.tender_round }}
    </h2>
    <div class="d-flex flex-column flex-grow overflow-hidden">
      <b-pagination
        v-model="centerRound"
        :total-rows="currentRound - 1"
        per-page="1"
        limit="10" 
        first-number
        last-number
        align="center"
        class="my-3"
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