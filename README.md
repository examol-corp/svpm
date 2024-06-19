# svpm

A tool to handle automated text replacement in your project in a safe
and controlled manner with built-in support for version manipulation
such as bumping and parsing.

NOTE: All descriptions here are not final as of now and are
descriptive of desired usage and behavior.

## Concepts

### What is a stencil?

A stencil is a special annotation in code comments that fences in a
piece of the file that can be manipulated in automation.

For instance if you have the following file `mypkg/__about__.py`:

```python
# svpm: START version
__version__ = "1.0.0"
# svpm: END version
```

The stencil name `version` is defined by the `# svpm: START` and
`#svpm: END` comments.

You can have multiple stencils in a file with different names. The
extra name for the stencil makes it so that you don't have to worry
about spurious matches within a file. For instance if you have a yaml
like:

```yaml
config:
  thinga:
    version: 0.1.2
  thingb:
    version: 1.2.3
```

Then a simple line based regex will not be able to distinguish between
them. One solution for some kinds of files is actual structural
knowledge. For yaml/json you can provide the path and the new text to
put there, e.g. `thinga.version` vs `thingb.version` for a tool like
`jq`.

Structural editing is always preferrable, but unfortunately not all
files are structured like this and it is unlikely that a single
general purpose tool could handle them all in a meaningful time
frame. So we provide a fully generic mechanism that can then be
augmented with structural editing tools as they become available.

The solution for the YAML file like above would be like this:

```yaml
config:
  thingA:
    # svpm: START thingAVersion
    version: 0.1.2
    # svpm: END thingAVersion

  thingB:
    # svpm: START thing_b_version
    version: 1.2
    # svpm: END thing_b_version
```

## Usage

### Replacing Stencils

Generic command to replace text in a stencil:

```shell
  svpm stencil replace mypkg/__about__.py::version '__version__ = "0.0.7"'
```


#### Replacing subpatterns in a stencil

Instead of replacing the entire stencil specify a pattern to match
within the stencil and the replacement text will fill in the
regions:

```shell
  svpm stencil replace \
       --pattern "__version__ = \"{r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"}\"" \
       mypkg/__about__.py::version \
       "0.0.7"
```

Subpatterns can also be specified inline for the stencil, e.g.:

```python
```python
# svpm: START version
# svpm: pattern __version = "^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$}"

__version__ = "1.0.0"
# svpm: END version
```

So that you don't need to specify it on invocation:

```shell
svpm stencil replace mypkg/__about__.py::version "0.0.7"
```


#### Built in subpatterns

Hauling common regexes for version numbers and similar patterns is
very error prone and annoying so we provide a suite of built-in
matching patterns. You can load which pattern templates you want
available (e.g. semver) and reference them by name in the pattern.

```shell
  svpm stencil replace \
       --templates semver \
       --pattern "__version__ = \"{semver_version}\"" \
       mypkg/__about__.py::version \
       "0.0.7"
```

IDEA: more fine-grained subpatterns for different versioning schemes,
see https://github.com/mbarkhau/bumpver for ideas.

### Transforming Stencils

`svpm` supports some standard tools for transforming stencils and
matched patterns.

We do not provide a "language" for doing this so much as we provide
fine-grained CLI tools which can be used to chain together in normal
unix fashion.

But some use cases are common enough that warrant built-in support
such as for version bumping.

#### Version Bumping

`svpm` provides built in support for bumping versions in specific stencils:

```shell
    # bump a specific version location using a placeholder instead of regex
    svpm stencil tr semver-bump \
         mypkg/__about__.py::version \
         "__version__ = \"{semver_version}\"" \
         patch
```

Replace a version with an explicit version, but using the convenient
placeholder:

```shell
    # bump a specific version location using a placeholder instead of regex
    svpm stencil tr semver \
         mypkg/__about__.py::version \
         "__version__ = \"{semver_version}\"" \
         patch
```

## Influences

- [bump](https://github.com/wader/bump)
- [bumpver](https://github.com/mbarkhau/bumpver)
