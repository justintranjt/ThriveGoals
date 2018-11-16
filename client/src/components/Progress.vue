<template>
	<div>
		<b-progress :value="value" :max=1 :precision="2" show-progress class="mb-3" variant="success"></b-progress>
	</div>
</template>

<script>
export default {
  props: ['value'],
};
</script>