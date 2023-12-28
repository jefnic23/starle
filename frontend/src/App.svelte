<script lang="ts">
	import { onMount } from "svelte";
	import { getAsync } from "./utils/http.util"
	import { getDateSeed } from "./utils/date.util";
    import { starles } from "./stores/game.store";
	import Game from "./components/Game.svelte";
	import type { Starle } from "./types/starle.type";

	onMount(async () => {
		// todo: save data to localStorage and prevent multiple api calls
		let data = await getAsync<Starle[]>(`/api/starle?seed=${getDateSeed()}`);
		console.log(data);
		starles.set(data);
	});
</script>

<main>
	<Game />
</main>

<style>
	
</style>
