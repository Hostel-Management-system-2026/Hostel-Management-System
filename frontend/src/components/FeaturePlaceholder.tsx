type Props = { title: string; description: string; endpoint: string }

export default function FeaturePlaceholder({ title, description, endpoint }: Props) {
  return (
    <section className="feature-placeholder">
      <div className="eyebrow">FEATURE WORKSPACE</div>
      <h2>{title}</h2>
      <p>{description}</p>
      <div className="contract-row">
        <span className="contract-dot" />
        <span>API contract</span>
        <code>{endpoint}</code>
      </div>
      <div className="placeholder-note">
        This page is ready for its feature implementation. Use the shared <code>api</code> client;
        keep authorization enforced by the backend.
      </div>
    </section>
  )
}
