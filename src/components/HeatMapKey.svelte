<script>
    export let colorScale;
    
    // Create gradient data points
    const gradientStops = [];
    for (let i = 0; i <= 100; i += 10) {
        const value = -6 + (i / 100) * 12; // Maps 0-100% to -6 to +6
        gradientStops.push({
            offset: `${i}%`,
            color: colorScale(value)
        });
    }
</script>

<div class="legend">
    <h3>Temperature Change</h3>
    <div class="gradient-container">
        <svg viewBox="0 0 300 40" class="gradient-svg">
            <defs>
                <linearGradient id="temperatureGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    {#each gradientStops as stop}
                        <stop offset={stop.offset} stop-color={stop.color} />
                    {/each}
                </linearGradient>
            </defs>
            <rect x="0" y="10" width="300" height="20" fill="url(#temperatureGradient)" stroke="#333" stroke-width="1" />
        </svg>
        <div class="labels">
            <span class="label-left">-8°F<br><small>Cooling</small></span>
            <span class="label-center">0°F<br><small>No Change</small></span>
            <span class="label-right">+6°F<br><small>Warming</small></span>
        </div>
    </div>
</div>

<style>
    .legend {
        text-align: center;
        margin-bottom: 20px;
        width: 100%;
        max-width: 300px;
        margin-left: auto;
        margin-right: auto;
    }
    
    h3 {
        color: white;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .gradient-container {
        position: relative;
        width: 100%;
    }
    
    .gradient-svg {
        width: 100%;
        height: auto;
        max-width: 300px;
    }
    
    .labels {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        width: 100%;
        font-size: 0.85rem;
        margin-bottom: 5px;
        color: rgba(255, 255, 255, 0.9);
    }
    
    .label-left {
        text-align: left;
        color: #93c5fd; /* Light blue */
    }
    
    .label-center {
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
    }
    
    .label-right {
        text-align: right;
        color: #fca5a5; /* Light red */
    }
    
    small {
        font-size: 0.7rem;
        opacity: 0.8;
        display: block;
        margin-top: 2px;
    }
    
    @media (max-width: 500px) {
        .legend {
            margin-bottom: 15px;
        }
        
        h3 {
            font-size: 0.8rem;
        }
        
        .labels {
            font-size: 0.75rem;
        }
        
        small {
            font-size: 0.65rem;
        }
    }
    
    @media (max-width: 350px) {
        .labels {
            font-size: 0.7rem;
        }
        
        small {
            font-size: 0.6rem;
        }
    }
</style>
