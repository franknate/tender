<template>
  <div
    v-if="currentTender"
    class="d-flex flex-column h-v90"
  >
    <h2 class="text-center mt-2">
      Tender {{ currentTender.datestr }} {{ currentTender.market }} {{ currentTender.direction }}-{{ currentTender.tender_round }}
    </h2>
    <div
      v-if="currentRound > 1"
      class="d-flex flex-column h-95"
    >
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
      <div class="container">
        <div class="row border header">
            <div class="col-3 col-md-2"></div>
            <div class="col-3 px-md-5">
              <span v-show="centerRound > 1">
                <label class="mb-0 py-1">price</label>
                <label class="mb-0 py-1 float-right">amount</label>
              </span>
            </div>
            <div class="col-3 px-md-5 bg-primary text-white">
                <label class="mb-0 py-1">price</label>
                <label class="mb-0 py-1 float-right">amount</label>
            </div>
            <div class="col-3 px-md-5">
              <span v-show="centerRound < 10">
                <label class="mb-0 py-1">price</label>
                <label class="mb-0 py-1 float-right">amount</label>
              </span>
            </div>
            <div class="col"></div>
        </div>
      </div>
      <BidRows :centerRound="centerRound" />
    </div>
    <div
      v-else
      class="container"
    >
      <h4>No results yet.</h4>
      <RoundUploader />
    </div>
  </div>
</template>


<script>
import BidRows from "./BidRows.vue"
import RoundUploader from "./RoundUploader.vue"

export default {
  components: {
    BidRows,
    RoundUploader
  },
  data() {
    return {
      centerRound: 1
    }
  },
  computed: {
    currentTender() {
      return this.$store.state.currentTender;
    },
    currentRound() {
      return this.currentTender.current_bid_round; 
    }
  }
}
</script>


<style scoped>

.h-v90 {
  height: 90vh;
}

.h-95 {
  height: 95%;
}

.active {
  font-weight: bold;
}

.disabled {
  color: blueviolet;
  pointer-events: none !important;
  cursor: default !important;
}

.header {
  overflow-y: scroll;
  scrollbar-width: thin;
}

.header::-webkit-scrollbar {
  width: 5px;
}

.header::-webkit-scrollbar-thumb {
  background: gray;
  border-radius: 3px;
}

</style>