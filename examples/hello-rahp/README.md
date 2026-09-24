# Hello RAHP

This is the smallest maintained adoption exercise. It uses **RAHP only**. DPIP and the Trust Protocol Interop Lab are not required.

## 1. Install RAHP dependencies

From the RAHP repository root:

~~~bash
pip install -r requirements.txt
~~~

## 2. Validate the onboarding configuration

~~~bash
python3 tools/rahp.py config-validate --config examples/hello-rahp/rahp.yaml
python3 tools/rahp.py targets --config examples/hello-rahp/rahp.yaml
~~~

The target is the bundled [sample specification](subject/spec.md). The configuration uses the current RAHP checkout as the source repository so the example can resolve an immutable Git commit without cloning another project.

## 3. Inspect the review command without creating working state

~~~bash
python3 tools/rahp.py review \
  --config examples/hello-rahp/rahp.yaml \
  --target hello-spec \
  --mode rahp \
  --offline \
  --dry-run
~~~

The dry run should resolve the current checkout commit and show the review scaffold command RAHP would execute.

## 4. Run the scaffold when you want to continue

Remove **--dry-run**:

~~~bash
python3 tools/rahp.py review \
  --config examples/hello-rahp/rahp.yaml \
  --target hello-spec \
  --mode rahp \
  --offline
~~~

This creates working review state under the ignored RAHP workspace. Command completion does not manufacture an assurance finding. Inspect the subject and substantiate any findings with the evidence required by the proposition.

## What you have learned

At this point you have exercised the minimum adoption boundary:

~~~text
bounded subject
  -> deployment configuration
  -> immutable source revision
  -> RAHP review entry point
~~~

No specialist assessor or external evidence producer was needed.

If your next assurance question concerns composed privacy, continue through the [adoption gateway](../../docs/adoption-guide.md) to DPIP. If the proposition requires executable interoperability or implementation evidence, use the same gateway to determine whether a compatible evidence producer such as the Trust Protocol Interop Lab is appropriate.

For the normal project adoption flow, continue with [Adopting RAHP](../../ADOPTION.md).
