interface AdBannerProps {
  className?: string;
}

export function AdBanner({ className }: AdBannerProps) {
  return (
    <div className={`ad-container ${className || ''}`}>
      <ins 
        className="adsbygoogle"
        style={{
          display: 'block',
          width: '100%',
          height: '250px'
        }}
        data-ad-client="ca-pub-5508768187151867"
        data-ad-slot="4067267701"
        data-ad-format="auto"
        data-full-width-responsive="true"
      />
    </div>
  );
}