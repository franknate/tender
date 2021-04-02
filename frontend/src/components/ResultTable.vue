<template>
  <div class="flex-grow container" id="table-wrapper">
    <table class="table text-center">
      <thead>
        <tr>
          <th class="sticky-header sticky-column bg-white" id="topLeft">Unit</th>
          <th v-for="i in 10" :key="i" class="sticky-header bg-white column">
            <span class="pr-4">Price</span>
            <span class="pl-4">Amount</span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(unit, index) in currentTender.units" :key="unit.id">
          <th class="sticky-column align-middle bg-light">
            {{ formatDate(unit.fromdate) }}<br>
            {{ formatDate(unit.todate) }}
          </th>
          <td v-for="i in 10" :key="i">
            <p v-for="bid in filterBids(unit, i)" :key="bid.id" class="m-0">
              <span class="pr-4">{{ bid.price }}</span>
              <span class="pr-4">{{ bid.amount }}</span>
            </p>
            <div v-if="currentRound == i && index == 0">
              <b-button variant="outline-primary" v-b-modal.modal-center>
                <b-icon icon="folder-plus"></b-icon>
              </b-button>
              <b-modal
                id="modal-center"
                title="Upload Results"
                centered
                hide-footer
              >
                <RoundUploader />
              </b-modal>
            </div>

          </td>
        </tr>
      </tbody>
    </table>
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
  data() {
    return {
      rowspan: 15
    }
  },
  methods: {
    filterBids(unit, round) {
      return unit.bids.filter(bid => bid.bid_round == this.currentTender.bid_rounds[round-1].id);
    },
    formatDate(date) {
      return new Date(date).toDateString().split(' ').slice(1).join(' ');
    }
  },
  computed: {
    currentTender() {
      return this.$store.getters.CurrentTender;
    },
    currentRound() {
      return this.currentTender.current_bid_round;
    }
  },
  watch: {
    centerRound(newRound, oldRound) {
      var columns = this.$el.querySelectorAll(".column");
      columns.forEach(el => {
        el.classList.remove("bg-primary")
        el.classList.add("bg-white")
        el.style.color = "black";
      })
      columns[newRound-1].classList.remove("bg-white")
      columns[newRound-1].classList.add("bg-primary")
      columns[newRound-1].style.color = "white"
      columns[newRound].scrollIntoView({
        behavior: "smooth",
        inline: "end"
      })
    }
  },
  mounted() {
    var columns = this.$el.querySelectorAll(".column");
    columns.forEach(el => {
      el.classList.remove('bg-primary')
      el.classList.add('bg-white')
      el.style.color = "black";
    })
    columns[0].classList.remove('bg-white')
    columns[0].classList.add('bg-primary')
    columns[0].style.color = "white"
    columns[0].scrollIntoView({
      inline: "end"
    })
  }
}
</script>

<style scoped>

table {
  width: 296%;
  border-spacing: 0;
  border-collapse: separate;
}
th {
  padding: 0;
  margin: 0;
}
#topLeft {
  z-index: 20;
  width: 5.4%;
}
#table-wrapper {
  overflow: auto;
  scrollbar-width: none;
  padding: 0;
}
#table-wrapper::-webkit-scrollbar {
  width: 0px;
}
.sticky-header {
  position: sticky;
  top: 0;
}
.sticky-column {
  position: sticky;
  left: 0;
}
.column {
  transition: all .2s;
}

</style>