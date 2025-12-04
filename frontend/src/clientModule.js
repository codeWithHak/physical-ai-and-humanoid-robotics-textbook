import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';

if (ExecutionEnvironment.canUseDOM) {
  // Defensive shim for Google Analytics
  // Prevents "window.gtag is not a function" crashes if the script is blocked (e.g. by adblockers)
  if (typeof window.gtag !== 'function') {
    window.gtag = function() {
      // console.log('Gtag shim called', arguments);
    };
  }
}
