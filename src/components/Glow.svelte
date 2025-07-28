<!-- SVG filter component for glow effect -->
<defs>
  <filter id="glow" height="130%">
    <feGaussianBlur in="SourceAlpha" stdDeviation="7.5" />
    <feOffset dx="0" dy="0" result="offsetblur" />
    <feFlood flood-color="rgb(250, 250, 250, 0.5)" />
    <feComposite in2="offsetblur" operator="in" />
    <feMerge>
      <feMergeNode />
      <feMergeNode in="SourceGraphic" />
    </feMerge>
  </filter>
</defs>