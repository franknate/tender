<template>
    <div
      class="container rounded border-top border-bottom"
      id="bidRows"
    >
      <div
        v-for="(unit, index) in currentTender.units"
        :key="unit.id"
        class="row bg-light border mb-1"
      >
        <div class="d-flex justify-content-center col-3 col-md-2 align-items-center shadow-x">
          {{ formatDate(unit.fromdate) }} <br>
          {{ formatDate(unit.todate) }}
        </div>
        <div class="col-3 px-md-5">
          <ul>
            <li v-for="bid in filterBids(unit, -1)" :key="bid.id" :class="{ 'text-success': bid.ours }">
              <span>
                {{ bid.price }}
              </span>
              <span class="float-right pr-3">
                {{ bid.amount }}
              </span>
            </li>
          </ul>
        </div>
        <div class="col-3 px-md-5 shadow-x">
          <ul>
            <li v-for="bid in filterBids(unit, 0)" :key="bid.id" :class="{ 'text-success': bid.ours }">
              <span>
                {{ bid.price }}
              </span>
              <span class="float-right pr-3">
                {{ bid.amount }}
              </span>
            </li>
          </ul>
        </div>
        <div class="col-3 px-md-5">
          <ul>
            <li v-for="bid in filterBids(unit, 1)" :key="bid.id" :class="{ 'text-success': bid.ours }">
              <span>
                {{ bid.price }}
              </span>
              <span class="float-right pr-3">
                {{ bid.amount }}
              </span>
            </li>
          </ul>
          <RoundUploader
            v-if="currentRound < 11 && index == 0"
            v-show="centerRound == currentRound - 1"
          />
        </div>
        <div class="col"></div>
      </div>
    </div>
</template>

<script>
import RoundUploader from "./RoundUploader.vue"

export default {
  components: {
    RoundUploader
  },
  props: {
    centerRound: Number
  },
  methods: {
    filterBids(unit, shift) {
      let roundToFilter = this.centerRound + shift
      if (roundToFilter < 1 || roundToFilter > 10 || roundToFilter > this.currentRound || !this.currentTender.bid_rounds) {
        return null
      } else {
        return unit.bids.filter(bid => bid.bid_round == this.currentTender.bid_rounds[roundToFilter].id);
      }
    },
    formatDate(date) {
      return new Date(date).toDateString().split(' ').slice(1).join(' ');
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

<style>
ul {
  list-style-type: none;
  padding-left: 0px;
  margin-bottom: 0px;
}

#bidRows {
  overflow-y: scroll;
  scrollbar-width: thin;
}

#bidRows::-webkit-scrollbar {
  width: 5px;
}

#bidRows::-webkit-scrollbar-thumb {
  background: gray;
  border-radius: 3px;
}

.shadow-x {
  box-shadow: 0 .5rem 1rem rgba(0,0,0,.15);
  box-shadow: 12px 0 15px -4px rgba(0,0,0,.15), -12px 0 8px -4px rgba(0,0,0,.15);
}
</style>