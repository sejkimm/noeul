import type { Register, ThemeSetArgs } from 'claude-code'

import { makeColors } from './make-colors.js'
import { PALETTE } from './palette.js'

const LOOK: ThemeSetArgs = { colors: makeColors(PALETTE).theme }

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.theme.set(LOOK)
    await $.command.register({ name: 'cc-theme-noeul', description: 'Put the noeul look back on' })
    await $.command.register({ name: 'cc-theme-off', description: 'Take the look off' })
    return next(e)
  })

  on('command.run', { command: 'cc-theme-noeul' }, async $ => {
    const set = await $.theme.set(LOOK)
    return { text: set.isDrawn ? 'the noeul look is on' : set.reason }
  })

  on('command.run', { command: 'cc-theme-off' }, async $ => {
    const cleared = await $.theme.clear()
    return { text: cleared.isDrawn ? 'the theme is still drawn' : cleared.reason }
  })
}
