<script lang="ts">
	import { onMount } from "svelte";
	import { getAsync } from "./utils/http.util"
	import { getDateSeed } from "./utils/date.util";
    import { starles, names } from "./stores/game.store";
	import Game from "./components/Game.svelte";
	import type { Starle } from "./types/starle.type";

	onMount(async () => {
		// todo: save data to localStorage and prevent multiple api calls
		let starles_data = await getAsync<Starle[]>(`/api/starle?seed=${getDateSeed()}`);
		starles.set(starles_data);

		let names_data = await getAsync<string[]>('/api/names');
		names.set(names_data);
	});
</script>

<main>
	<Game />
</main>

<style>
	
</style>
