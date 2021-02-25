<template>
  <div>
    <b-button pill variant="outline-secondary" v-b-toggle.sidebar-right id="right-button">
        <b-icon icon="pen-fill"></b-icon>
    </b-button>
    <b-sidebar id="sidebar-right" title="Right" right>
      <div class="px-3 py-2">
        <p>
          Cras mattis consectetur purus sit amet fermentum. Cras justo odio, dapibus ac facilisis
          in, egestas eget quam. Morbi leo risus, porta ac consectetur ac, vestibulum at eros.
        </p>
      </div>
    </b-sidebar>
  </div>
</template>

<script>
export default {

}
</script>

<style>
#right-button {
  position: fixed;
  bottom: 50%;
  right: 1%;
}
</style>