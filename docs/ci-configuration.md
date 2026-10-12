# Disposable staging qualification

`staging-deploy.yml` tests mock and live profiles in disposable runner-owned stacks. It does not install a durable staging environment. Configure the repository secret `OPENROUTER_API_KEY` for the live profile; never put the key in dispatch inputs. The mock profile does not receive the secret.

Each profile uses a unique Compose project, private networks and volumes, generated container names, and an ephemeral loopback API port. A containerized runner joins only its profile's private network for health and smoke checks. Cleanup disconnects that network, removes only the profile's stack and volumes, and deletes the temporary credential and rendered Compose files.

Keep the existing full CI quality gate. Artifact uploads use the estate-qualified Gitea transport. Source checks and disposable smoke success do not prove durable deployment or live-provider approval.
