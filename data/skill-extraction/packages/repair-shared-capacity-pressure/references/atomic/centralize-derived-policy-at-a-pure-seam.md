# Atomic: centralize derived policy at a pure seam

## Problem

Preview, warning, and runtime state installation independently reproduce derived policy logic, so displayed thresholds can diverge from the threshold actually installed.

## Solution paradigm

Move pure derivation into one seam, return the complete derived result, project preview/warning from that result, and install the same result. Keep runtime-only auxiliary parameters outside the pure derivation when they do not belong to the invariant.

## Invariant

The policy reported to the user and the policy installed in runtime are equal for the same semantic inputs.

## Oracle

A model-switch guard's reported threshold must equal the compressor's installed threshold; cap annotations appear only when the cap actually binds.

## Realization

Hermes commit `af0be164c1d287ebc742d1b8376d82e5fb42fda5`.

This is an implementation-architecture Atomic, not evidence for the residual-capacity Pattern by itself.
