<template>
  <div
    v-if="currentTender"
    id="centerBox"
    class="d-flex flex-column"
  >
    <h2 class="text-center mt-2">
      Tender {{ currentTender.date }} {{ currentTender.market }} {{ currentTender.direction }}-{{ currentTender.tender_round }}
    </h2>
    <b-pagination
      v-model="currentRound"
      :total-rows="lastRound"
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
            <span v-show="currentRound > 1">
              <label class="mb-0 py-1">price</label>
              <label class="mb-0 py-1 float-right">amount</label>
            </span>
          </div>
          <div class="col-3 px-md-5 bg-primary text-white">
              <label class="mb-0 py-1">price</label>
              <label class="mb-0 py-1 float-right">amount</label>
          </div>
          <div class="col-3 px-md-5">
            <span v-show="currentRound < 10">
              <label class="mb-0 py-1">price</label>
              <label class="mb-0 py-1 float-right">amount</label>
            </span>
          </div>
          <div class="col"></div>
      </div>
    </div>
    <BidRows :lastRound="lastRound" />
  </div>
</template>


<script>
import BidRows from "./BidRows.vue"

export default {
  components: {
    BidRows
  },
  methods: {
    shouldDisable(page) {
      return page > this.lastRound;
    }
  },
  computed: {
    currentTender() {
      return this.$store.state.currentTender;
    },
    currentRound: {
      get() {
        return this.$store.state.currentRound;
      },
      set(value) {
        this.$store.commit("switchRound", value)
      }      
    },
    lastRound() {
      var bids = this.currentTender.units[0].bids;
      return bids[bids.length-1].bid_round;
    }
  },
  created() {
    this.$store.commit("switchTender", 8)
  }
}
</script>


<style scoped>

#centerBox {
  height: 90vh;
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