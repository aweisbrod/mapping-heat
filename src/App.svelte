<script>
  import world from "$data/world-110m.json";
  import * as topojson from "topojson-client";

  // Force reload - Updated with 123 countries (Jul 22, 2025)
  console.log(world);
  
  // Create countries and borders from the world data
  let countries = topojson.feature(world, world.objects.countries).features;
  let borders = topojson.mesh(world, world.objects.countries, (a, b) => a !== b);

  console.log(countries);
  console.log(borders);

  // Projection function — orthographic projection. Create countries and borders
  import { geoOrthographic, geoPath, geoCentroid } from "d3-geo";

  let width = 400;
  let containerWidth = 400;
  let zoomScale = spring(1, { stiffness: 0.1, damping: 0.8 });
  
  // Make width responsive to container but with max size
  $: width = Math.min(containerWidth, 468);
  $: height = width;

  $: projection = geoOrthographic()
    .scale((width / 2) * $zoomScale) // Apply zoom scale to the base scale
    .rotate([$xRotation, $yRotation, 0]) // How it should rotate on an x, y, z axis
    .translate([width / 2, height / 2]); // Where the projection is centered on the screen

  // Create path generator that will draw our shapes
  $: path = geoPath(projection);

  // Import the Glow component
  import Glow from "./components/Glow.svelte";

  // Import color scale and heat index data
  import {scaleLinear} from "d3-scale";
  import { max } from "d3-array";

  import data from "$data/heat_index_by_country.json";
  import countryMapping from "$data/country-id-mapping.json";
  
  // Modify countries array to include heat index data
  countries.forEach((country) => {
    // Map numerical ID to 3-letter country code
    const countryCode = countryMapping[country.id];
    if (countryCode) {
      // Always assign the country code so tooltip can display country name
      country.country_code = countryCode;
      
      // Check if this is LUX or BEL (insufficient data)
      if (countryCode === 'LUX' || countryCode === 'BEL') {
        country.insufficient_data = true;
        country.country_name = countryCode === 'LUX' ? 'Luxembourg' : 'Belgium';
      } else {
        // Find heat index data for other countries
        const heatData = data?.find((d) => d.country_code === countryCode);
        if (heatData) {
          country.heat_index_2000 = heatData.heat_index_2000;
          country.heat_index_2025 = heatData.heat_index_2025;
          country.difference = heatData.difference;
          country.percent_change = heatData.percent_change;
          country.country_name = heatData.country_name;
          country.data_points = heatData.data_points;
        }
      }
    } else if (!country.id || country.id === '-99' || (country.properties && Object.values(country.properties).includes(-99))) {
      // Handle regions without IDs, with ID '-99', or with -99 properties (unmapped territories)
      // For regions with -99 properties or ID in Africa, assume it's part of Somalia
      country.country_code = 'SOM';
    }
  });

  // Create a color scale for temperature difference (warming/cooling)
  const colorScale = scaleLinear()
    .domain([-6, 0, 6]) // -6°F cooling to +6°F warming
    .range(["#2563eb", "#f8fafc", "#dc2626"]); // Blue (cooling) to White to Red (warming)

  // Autorotate the globe and spring
  import {timer} from "d3-timer";
  import {spring} from "svelte/motion";
  
  let xRotation = spring(0, { stiffness: 0.08, damping: 0.4 });
  let yRotation = spring(0, { stiffness: 0.1, damping: 0.8 });
  let degreesPerFrame = 0.5;

  // Timer to update xRotation
  const t = timer((elapsed) => {
    if (dragging || tooltipData) return; // If dragging, do not rotate
    $xRotation += degreesPerFrame;
    // yRotation stays at 0 - removed the increment
  }, 0);

  // User interaction 
  let globe;
 //Import onMount from svelte
  import { onMount } from "svelte";
  // Import drag and zoom from d3
  import {drag} from "d3-drag";
  import {zoom} from "d3-zoom";
  import {select} from "d3-selection";

  const dragSensitivity = 1;
  const zoomSensitivity = 0.1;
  let dragging = false;
  
  onMount (() =>{
    const element = select(globe);
    
    // Add drag behavior
    element.call(
      drag().on("drag", (event) => {
        $xRotation = $xRotation + event.dx * dragSensitivity;
        $yRotation = $yRotation - event.dy * dragSensitivity;
        dragging = true;
      })
      .on("end", () => {
        dragging = false;
      })
    );

    // Add zoom behavior
    element.call(
      zoom()
        .scaleExtent([0.5, 5]) // Min and max zoom levels
        .on("zoom", (event) => {
          $zoomScale = event.transform.k;
        })
    );
  })


// Tooltip
let tooltipData;
import Tooltip from "./components/Tooltip.svelte";

// Legend component
import HeatMapKey from "./components/HeatMapKey.svelte";

// Import geoCentroid to calculate the center of the hovered country
$: if (tooltipData) {
  const center = geoCentroid(tooltipData);
  $xRotation = -center[0];
  $yRotation = -center[1];
  
}

// Draw the borders when focused
import {draw} from "svelte/transition"

$: countryCode = countryMapping[tooltipData?.id] || tooltipData?.country_code || null;

// Zoom control functions
function zoomIn() {
  $zoomScale = Math.min($zoomScale * 1.5, 5);
}

function zoomOut() {
  $zoomScale = Math.max($zoomScale / 1.5, 0.5);
}

function resetZoom() {
  $zoomScale = 1;
}

</script>

<div class="header">
  <h1>Heat indexes increased up to 5.5°F over the past 25 years</h1>
  <h2>Comparing July 2000 to July 2025, the data reveals significant warming and cooling trends across many regions.</h2>
  <br>
  <h3>Click on a country to see temperature change data. Drag the globe to rotate it. Source: Copernicus Climate Data Store.</h3>
</div>

<div class="chart-container" bind:clientWidth={containerWidth}>
    

  <!-- Legend -->
  <HeatMapKey {colorScale}/>
  <br>

  <!-- Zoom Controls -->
  <div class="zoom-controls">
    <button on:click={zoomIn} title="Zoom In">+</button>
    <button on:click={resetZoom} title="Reset Zoom">⌂</button>
    <button on:click={zoomOut} title="Zoom Out">−</button>
  </div>
  
  <svg viewBox="0 0 {width} {height}" bind:this={globe} class:dragging class="globe-svg">

    <!-- Define clipping path to contain zoom overflow -->
    <defs>
      <clipPath id="globe-clip">
        <rect x="-30" y="-30" width={width + 50} height={height + 50} />
      </clipPath>
    </defs>
    
    <!-- Glow -->
    <Glow />

    <!-- Globe content group with clipping -->
    <g clip-path="url(#globe-clip)">
      <!-- Globe background -->
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
      <circle
        cx={width / 2}
        cy={height / 2}
        r={(width / 2) * $zoomScale}
        fill="#1c1c1c"
        filter="url(#glow)"
        on:click={() => {
          tooltipData = null; // Clear tooltip when clicking on the background
        }}
      />

      <!-- Countries -->
      {#each countries.sort((a, b) => (b.difference || 0) - (a.difference || 0)) as country} 
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
         <!-- If insufficient data, show gray color -->
        <path d={path(country)} 
        fill={country.insufficient_data ? "rgb(60, 60, 60)" : (country.difference ? colorScale(country.difference) : "rgb(60, 60, 60)")}
        stroke="none"
        on:click={() => {
          tooltipData = country;
        }}
        on:focus={() => {
          tooltipData = country;
        }}
        tabindex="0"

        />
      {/each}

      <!-- Borders -->
      <path d={path(borders)} 
        fill="none"
        stroke="black"
      />

      <!-- Selected border -->
      {#if tooltipData}
      {#key tooltipData.id}
        <path d={path(tooltipData)} 
          fill="none"
          stroke="white"
          stroke-width="2"
          in:draw
        />
      {/key}
      {/if}
    </g>
  </svg>
  <Tooltip data={tooltipData} />
</div>

<style>
  h1 {
    color: white;
    font-size: 2rem;
    font-weight: 800;
    line-height: 38px;;
    margin-bottom: 0.5rem;
  }

  h2 {
    font-size: 1.25rem;
    font-weight: 200;
    line-height: 24px;
    color: white;
    margin-bottom: 0.25rem;
  }

  h3 {
    font-size: 1rem;
    color: rgba(255, 255, 255, 0.8);
    line-height: 20px;
    margin-bottom: 1rem;
  }

  .header {
    max-width: 600px;
    margin: 4rem auto;
    padding: 0 20px;
  }

  @media (max-width: 640px) {
    .header {
      margin: 2rem auto;
      padding: 0 4rem;
    }
    
    h1 {
      font-size: 1.5rem;
      line-height: 32px;
    }
    
    h2 {
      font-size: 1.125rem;
      line-height: 22px;
    }
  }

  p {
    color: rgba(255, 255, 255, 0.8);
    font-size: 0.9rem;
  }
  
  .chart-container {
    max-width: 468px;
    width: 100%;
    height: auto;
    margin: 0 auto;
    position: relative;
    padding: 0 20px;
  }

  @media (max-width: 500px) {
    .chart-container {
      width: 80%;
      height: auto;
    }
  }

  .zoom-controls {
    position: absolute;
    bottom: 10px;
    right: 10px;
    z-index: 10;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }

  @media (max-width: 500px) {
    .zoom-controls {
      right: 5px;
      bottom: 5px;
    }
  }

  .zoom-controls button {
    width: 25px;
    height: 25px;
    border: 2px solid #fff;
    background: rgba(40, 40, 40, 0.9);
    color: #fff;
    border-radius: 5px;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
  }

  .zoom-controls button:hover {
    background: rgba(60, 60, 60, 0.9);
    transform: scale(1.05);
  }

  .zoom-controls button:active {
    transform: scale(0.95);
  }

  .globe-svg {
    width: 100%;
    height: auto;
    max-width: 468px;
    
  }

  svg, path:focus {
    overflow: visible;
  }

  .dragging {
    cursor: grab;
  }

  path {
    cursor: pointer;
  }

  /* Remove outline when path is focused. Typically a bad idea, but we're already highlighting the path */
  path:focus {
    outline: none;
  }
</style>