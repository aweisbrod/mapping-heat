<script>
    export let data;
    import {format} from "d3-format";
    const suffixFormat = (d) => format(".2s")(d).replace("G", "B");

    import {fade} from "svelte/transition";
    
    // Function to get country name from country code for countries without heat index data
    const getCountryName = (countryCode) => {
        const countryNames = {
            'ARG': 'Argentina',
            'PER': 'Peru', 
            'CHL': 'Chile',
            'ECU': 'Ecuador',
            'BOL': 'Bolivia',
            'URY': 'Uruguay',
            'PRY': 'Paraguay',
            'CAN': 'Canada',
            'GRL': 'Greenland',
            'ISL': 'Iceland',
            'MNG': 'Mongolia',
            'KAZ': 'Kazakhstan',
            'RUS': 'Russia',
            'ATA': 'Antarctica',
            'WSM': 'Yemen',
            'YEM': 'Yemen',
            'SOM': 'Somalia',
            'NZL': 'New Zealand',
            'SOL': 'Somalia',
            'SO': 'Somalia',
            'SOM1': 'Somalia',
            'SOMLAND': 'Somalia',
            'UN': 'Somalia',
            'UNKNOWN': 'Somalia',
            'TWN': 'Taiwan',
            'ATF': 'French Southern Territories',
            'BEN': 'Benin',
            'BHS': 'Bahamas',
            'BLR': 'Belarus',
            'BLZ': 'Belize',
            'CMR': 'Cameroon',
            'COG': 'Congo',
            'CRI': 'Costa Rica',
            'CUB': 'Cuba',
            'CYP': 'Cyprus',
            'DNK': 'Denmark',
            'DOM': 'Dominican Republic',
            'EST': 'Estonia',
            'FLK': 'Falkland Islands',
            'GAB': 'Gabon',
            'GBR': 'United Kingdom',
            'GIN': 'Guinea',
            'GMB': 'Gambia',
            'GNB': 'Guinea-Bissau',
            'GNQ': 'Equatorial Guinea',
            'GTM': 'Guatemala',
            'HND': 'Honduras',
            'HTI': 'Haiti',
            'IRL': 'Ireland',
            'JAM': 'Jamaica',
            'LBR': 'Liberia',
            'LSO': 'Lesotho',
            'LVA': 'Latvia',
            'MDA': 'Moldova',
            'MRT': 'Mauritania',
            'NCL': 'New Caledonia',
            'NIC': 'Nicaragua',
            'NLD': 'Netherlands',
            'PAN': 'Panama',
            'PRI': 'Puerto Rico',
            'ESH': 'Western Sahara',
            'SEN': 'Senegal',
            'SLB': 'Solomon Islands',
            'SLV': 'El Salvador',
            'SLE': 'Sierra Leone',
            'SWZ': 'Eswatini',
            'TGO': 'Togo',
            'TLS': 'Timor-Leste',
            'TTO': 'Trinidad and Tobago',
            'VUT': 'Vanuatu',
            // Add more as needed
        };
        return countryNames[countryCode] || countryCode;
    };
    
    // Function to get explanation for missing data
    // const getNoDataExplanation = (countryCode) => {
    //     const explanations = {
    //         'ARG': 'Heat index requires both high temperature and humidity. Argentina\'s temperate climate and high-altitude regions typically don\'t meet these conditions.',
    //         'PER': 'Peru\'s high-altitude Andes mountains and coastal desert regions don\'t typically experience the hot, humid conditions needed for heat index calculations.',
    //         'CHL': 'Chile\'s Atacama Desert and high-altitude regions have dry conditions unsuitable for heat index measurements.',
    //         'ECU': 'Ecuador\'s high-altitude regions (like Quito at 9,350ft) have cooler temperatures that don\'t require heat index calculations.',
    //         'BOL': 'Bolivia\'s high-altitude plateau climate doesn\'t typically reach the hot, humid conditions needed for heat index.',
    //         'URY': 'Uruguay\'s temperate oceanic climate rarely reaches the combination of high heat and humidity required for heat index.',
    //         'PRY': 'Paraguay\'s climate data may be limited in the dataset.',
    //         'GRL': 'Greenland\'s Arctic climate doesn\'t reach temperatures where heat index is applicable.',
    //         'ISL': 'Iceland\'s cool climate doesn\'t require heat index calculations.',
    //         'MNG': 'Mongolia\'s dry continental climate typically lacks the humidity needed for heat index measurements.',
    //     };
    //     return explanations[countryCode] || 'Heat index data not available for this region. This typically occurs in areas with dry climates, high altitudes, or cooler temperatures where heat index calculations don\'t apply.';
    // };
    
    // Determine display name and whether we have data
    $: displayName = data?.country_name || (data?.country_code ? getCountryName(data.country_code) : 'Unknown Country');
    $: hasData = data?.heat_index_2000 && data?.heat_index_2025;
    $: hasInsufficientData = data?.insufficient_data;
    
    // Check if this is the disputed boundary region (ID -99 with SOM country code but no country_name)
    $: isDisputedBoundary = data?.country_code === 'SOM' && !data?.country_name && data?.id === '-99';
    $: finalDisplayName = isDisputedBoundary ? `${displayName} (disputed boundary)` : displayName;
</script>

{#if data}
    <div transition:fade>
        {#if hasData}
            <h2>{finalDisplayName}</h2>
            <h3>2000: {data.heat_index_2000.toFixed(1)}°F</h3>
            <h3>2025: {data.heat_index_2025.toFixed(1)}°F</h3>
            <h3 class="change {data.difference > 0 ? 'warming' : 'cooling'}">
                Change: {(data.difference > 0 ? '+' : '') + data.difference.toFixed(1)}°F
            </h3>
        {:else if hasInsufficientData}
            <h2>{finalDisplayName}</h2>
            <h3 class="no-data-title">Insufficient Data</h3>
        {:else}
            <h2>{finalDisplayName}</h2>
            <h3 class="no-data-title">No Heat Index Data</h3>
            <!-- <p class="explanation">{getNoDataExplanation(data.country_code)}</p> -->
        {/if}
    </div>
{/if}

<style>
    div {
        position: absolute;
        bottom: -100px;
        left: 0px;
        text-align: left;
        min-width: 250px;
        max-width: 350px;
        padding: 0 20px;
    }

    h2 {
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.25rem;
    }

    h3 {
        font-size: 1.2rem;
        font-weight: 400;
        color: rgba(255, 255, 255, 0.8);
        margin: 0;
        margin-bottom: 0.1rem;
    }

    h3.change {
        font-weight: 600;
        font-size: 1.3rem;
    }

    h3.warming {
        color: #fca5a5; /* Light red for warming */
    }

    h3.cooling {
        color: #93c5fd; /* Light blue for cooling */
    }

    h4 {
        font-size: 1rem;
        font-weight: 300;
        color: rgba(255, 255, 255, 0.6);
        margin: 0;
    }

    .no-data-title {
        font-size: 1.1rem;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 0.5rem;
    }

    /* Responsive design for smaller screens */
    @media (max-width: 640px) {
        div {
            left: 40px; /* Larger left margin on mobile */
            min-width: 200px;
            max-width: 280px;
            padding: 0 15px;
        }
        
        h2 {
            font-size: 1.3rem;
        }
        
        h3 {
            font-size: 1.1rem;
        }
        
        h3.change {
            font-size: 1.2rem;
        }
        
        h4 {
            font-size: 0.9rem;
        }
    }
    
    @media (max-width: 480px) {
        div {
            left: 60px; /* Even larger left margin on very small screens */
            min-width: 180px;
            max-width: 240px;
            padding: 0 10px;
        }
        
        h2 {
            font-size: 1.2rem;
        }
        
        h3 {
            font-size: 1rem;
        }
        
        h3.change {
            font-size: 1.1rem;
        }
        
        h4 {
            font-size: 0.85rem;
        }
        
        .no-data-title {
            font-size: 1rem;
        }
    }
    
    @media (max-width: 350px) {
        div {
            left: 80px; /* Maximum left margin for very narrow screens */
            min-width: 160px;
            max-width: 200px;
        }
        
        h2 {
            font-size: 1.1rem;
        }
        
        h3 {
            font-size: 0.95rem;
        }
        
        h3.change {
            font-size: 1rem;
        }
        
        h4 {
            font-size: 0.8rem;
        }
    }

</style>