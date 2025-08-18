"use client"

import { useEffect, useState } from "react"

export function ParticleBackground() {
  const [particles, setParticles] = useState<
    Array<{
      id: number
      left: string
      top: string
      delay: string
      duration: string
    }>
  >([])

  useEffect(() => {
    const newParticles = Array.from({ length: 25 }, (_, i) => ({
      id: i,
      left: `${Math.random() * 100}%`,
      top: `${Math.random() * 100}%`,
      delay: `${Math.random() * 5}s`,
      duration: `${4 + Math.random() * 3}s`,
    }))

    setParticles(newParticles)
  }, [])

  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
      {particles.map((particle) => (
        <div
          key={particle.id}
          className="absolute w-1 h-1 rounded-full opacity-30"
          style={{
            left: particle.left,
            top: particle.top,
            animationDelay: particle.delay,
            animationDuration: particle.duration,
            background: "#D0FF16",
            boxShadow: "0 0 6px rgba(208, 255, 22, 0.4)",
            animation: `float ${particle.duration} ease-in-out infinite`,
          }}
        />
      ))}

      <div className="absolute inset-0">
        <div
          className="absolute w-96 h-96 rounded-full opacity-5"
          style={{
            background: "radial-gradient(circle, rgba(208, 255, 22, 0.1) 0%, transparent 70%)",
            top: "10%",
            left: "10%",
            animation: "float 20s ease-in-out infinite",
          }}
        />
        <div
          className="absolute w-64 h-64 rounded-full opacity-5"
          style={{
            background: "radial-gradient(circle, rgba(208, 255, 22, 0.1) 0%, transparent 70%)",
            top: "60%",
            right: "15%",
            animation: "float 25s ease-in-out infinite reverse",
          }}
        />
        <div
          className="absolute w-80 h-80 rounded-full opacity-5"
          style={{
            background: "radial-gradient(circle, rgba(208, 255, 22, 0.1) 0%, transparent 70%)",
            bottom: "20%",
            left: "20%",
            animation: "float 30s ease-in-out infinite",
          }}
        />
      </div>

      <style jsx>{`
        @keyframes float {
          0%, 100% {
            transform: translateY(0px) rotate(0deg);
            opacity: 0.3;
          }
          50% {
            transform: translateY(-30px) rotate(180deg);
            opacity: 0.6;
          }
        }
      `}</style>
    </div>
  )
}
